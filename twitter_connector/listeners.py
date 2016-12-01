from datetime import datetime
import json
import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import tweepy

from twitter_connector.models import Tweet, Url, Hashtag, HashtagUrl, TweetUrl
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

    def __init__(self):
        super().__init__()
        self.filter = ['created_at', 'entities', 'favorite_count', 'id',
                       'retweet_count', 'text', 'timestamp_ms']

    def parse_tweet(self, tweet, *args):
        data = {}
        for arg in args:
            try:
                data[arg] = tweet[arg]
            except KeyError:
                logger.error('No %s found on tweet' % arg)
                if arg == 'created_at':
                    data[arg] = timezone.now()
                    logger.info('Using current datetime %s.' % data[arg])
                else:
                    logger.error('Exiting so we can catch and fix the error',
                                 exec_info=True)
                    exit(1)
        return data

    def save_tweet(self, data, urls):
        try:
            tweet = Tweet.objects.get(pk=data['id'])
            _urls = [url.expanded_url for url in tweet.urls]
            for url in urls:
                if url.expanded_url not in _urls:
                    tweet.urls.append(url)
        except ObjectDoesNotExist:
            created_at = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S %z %Y')
            tweet = Tweet(
                id=data['id'], created_at=created_at, text=data['text'],
                timestamp_ms=data['timestamp_ms'], retweet_count=data['retweet_count'],
                favorite_count=data['favorite_count']
            )
            tweet.save()
            for url in urls:
                tweet_url = TweetUrl()
                tweet_url.tweet = tweet
                tweet_url.url = url
                tweet_url.save()
                tweet.tweeturl_set.add(tweet_url)

        return tweet

    def get_urls(self, urls):
        expanded_urls = []
        urls_lst = []
        for url in urls:
            if url['url']:
                exp_url = get_expanded_url(url['expanded_url'])
                if exp_url not in urls_lst:
                    urls_lst.append(exp_url)
                    expanded_url = Url.objects.filter(expanded_url=exp_url).first()
                    if expanded_url:
                        expanded_url.modified_at = timezone.now()
                        expanded_urls.append(expanded_url)
                    else:
                        _url = Url.objects.filter(expanded_url=url['expanded_url']).first()
                        if not _url:
                            new_url = Url()
                            new_url.url = url['url']
                            new_url.expanded_url = exp_url
                            expanded_urls.append(new_url)
                        else:
                            logger.warn('Found matching url but different '
                                        'expanded_url. Skipping...')
        return expanded_urls

    def save_hashtags(self, hashtags):
        hashtags = []
        _hashtags = []
        for hashtag in hashtags:
            _tag = hashtag['text'].lower()
            if _tag not in _hashtags:
                _hashtags.append(_tag)
                tag = Hashtag.objects.filter(hashtag=_tag).first()
                if tag:
                    hashtags.append(tag)
                else:
                    new_tag = Hashtag()
                    new_tag.hashtag = _tag
                    new_tag.save()
                    hashtags.append(new_tag)
        return hashtags

    def save_urls(self, hashtags, urls):
        for url in urls:
            url.save()
            for hashtag in hashtags:
                if not url.hashtagurl_set.all().filter(hashtag=hashtag):
                    hashtag_url = HashtagUrl()
                    hashtag_url.hashtag = hashtag
                    hashtag_url.url = url
                    hashtag_url.save()
                    url.hashtagurl_set.add(hashtag_url)
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
            hashtags = self.save_hashtags(entities['hashtags'])
            urls = self.save_urls(hashtags, urls)
            tweet = self.save_tweet(data, urls)
            logger.info('Tweet Saved: %s' % tweet.text)
        return True

    def on_error(self, status):
        logger.error(status)
