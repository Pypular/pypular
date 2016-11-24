import tweepy
import json
import logging
import twitter_connector.models as db

from datetime import datetime
from twitter_connector.utils import get_expanded_url

logger = logging.getLogger(__name__)


class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


class FileListener(tweepy.StreamListener):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        logger.info('Opening file %s' % self.file_name)
        self.file = open(self.file_name, 'w')

    def __exit__(self):
        self.file.close()
        logger.info('Closing file %s' % self.file_name)

    def on_data(self, data):
        self.file.write(data)
        return True

    def on_error(self, status):
        logger.error(status, exec_info=True)


class DBListener(tweepy.StreamListener):

    def __init__(self, db_name):
        super().__init__()
        self.filter = ['created_at', 'entities', 'favorite_count', 'id',
                       'retweet_count', 'text', 'timestamp_ms']
        self.db_name = db_name
        self.session = db.setup_db()

    def __exit__(self):
        self.session.close()
        logger.info('Closing connection with DB %s' % self.db_name)

    def parse_tweet(self, tweet, *args):
        data = {}
        for arg in args:
            try:
                data[arg] = tweet[arg]
            except KeyError:
                logger.error('No %s found on tweet' % arg)
                if arg == 'created_at':
                    data[arg] = datetime.utcnow()
                    logger.info('Using current datetime %s.' % data[arg])
                else:
                    logger.error('Exiting so we can catch and fix the error',
                                 exec_info=True)
                    exit(1)
        return data

    def get_tweets(self, data, urls):
        tweet = self.session.query(db.Tweet).filter_by(id=data['id']).first()
        if tweet:
            _urls = [url.expanded_url for url in tweet.urls]
            for url in urls:
                if url.expanded_url not in _urls:
                    tweet.urls.append(url)
        else:
            tweet = db.Tweet(
                id=data['id'], created_at=data['created_at'], timestamp_ms=data['timestamp_ms'],
                text=data['text'], urls=urls, retweet_count=data['retweet_count'],
                favorite_count=data['favorite_count']
            )
        return tweet

    def get_urls(self, urls):
        expanded_urls = []
        urls_lst = []
        for url in urls:
            exp_url = get_expanded_url(url['expanded_url'])
            if exp_url not in urls_lst:
                urls_lst.append(exp_url)
                expanded_url = self.session.query(db.Url).filter_by(
                    expanded_url=exp_url).first()
                if expanded_url:
                    expanded_url.modified_at = datetime.utcnow()
                    expanded_urls.append(expanded_url)
                else:
                    _url = self.session.query(db.Url).filter_by(
                        url=url['expanded_url']).first()
                    if not _url:
                        new_url = db.Url(url['expanded_url'])
                        new_url.expanded_url = exp_url
                        expanded_urls.append(new_url)
                    else:
                        logger.warn('Found matching url but different '
                                    'expanded_url. Skipping...')
        return expanded_urls

    def get_hashtags(self, entities):
        hashtags = []
        _hashtags = []
        for hashtag in entities['hashtags']:
            _tag = hashtag['text'].lower()
            if _tag not in _hashtags:
                _hashtags.append(_tag)
                tag = self.session.query(db.Hashtag).filter_by(hashtag=_tag).first()
                if tag:
                    # tag.urls.append(urls)
                    hashtags.append(tag)
                else:
                    new_tag = db.Hashtag(_tag)
                    # new_tag.urls = urls
                    hashtags.append(new_tag)
        return hashtags

    def add_hashtags(self, hashtags, urls):
        for url in urls:
            tags = url.hashtags
            for hashtag in hashtags:
                if hashtag not in tags:
                    url.hashtags.append(hashtag)
        return urls

    def on_data(self, raw_data):
        try:
            json_tweet = json.loads(raw_data)
        except TypeError:
            logger.error('Error reading tweet:', exc_info=True)
            return True
        data = self.parse_tweet(json_tweet, *self.filter)
        entities = data['entities']
        urls = self.get_urls(entities['urls'])
        if urls:
            print('************ URLS **********: ', urls)
            hashtags = self.get_hashtags(entities)
            urls = self.add_hashtags(hashtags, urls)
            tweet = self.get_tweets(data, urls)
            logger.info('Saving Tweet: %s' % tweet.text)
            self.session.add(tweet)
            self.session.add_all(hashtags)
            self.session.add_all(urls)
            self.session.commit()
        return True

    def on_error(self, status):
        logger.error(status)
