
import tweepy
import json
import logging

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from twitter_connector.models import Tweet, Url, Hashtag
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
                    data[arg] = datetime.utcnow()
                    logger.info('Using current datetime %s.' % data[arg])
                else:
                    logger.error('Exiting so we can catch and fix the error',
                                 exec_info=True)
                    exit(1)
        return data

    def save_tweet(self, data, urls, hashtags):
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
            tweet.save(urls=urls, hashtags=hashtags)

        return tweet

    def prepare_urls(self, urls):
        urls_to_save = {}
        for url in urls:
            if url['url']:
                exp_url = get_expanded_url(url['expanded_url'])
                if exp_url not in urls_to_save.keys():
                    try:
                        new_url = Url.objects.get(expanded_url=exp_url)
                        new_url.modified_at = datetime.utcnow()
                        urls_to_save[exp_url] = new_url
                    except ObjectDoesNotExist:
                        try:
                            Url.objects.get(url=url['expanded_url'])
                            logger.warn('Found matching url but different '
                                        'expanded_url. Skipping...')
                        except ObjectDoesNotExist:
                            new_url = Url()
                            new_url.url = url['url']
                            new_url.expanded_url = exp_url
                            urls_to_save[exp_url] = new_url

        return urls_to_save.values()

    def prepare_hashtags(self, hashtags):
        hashtag_list = []
        for tag in hashtags:
            if tag not in hashtag_list:
                try:
                    new_tag = Hashtag.objects.get(hashtag=tag)
                except ObjectDoesNotExist:
                    new_tag = Hashtag()
                    new_tag.hashtag = tag

                hashtag_list.append(new_tag)

        return hashtag_list

    def on_data(self, raw_data):
        try:
            json_tweet = json.loads(raw_data)
        except TypeError:
            logger.error('Error reading tweet:', exc_info=True)
            return True
        data = self.parse_tweet(json_tweet, *self.filter)
        entities = data['entities']
        urls = self.prepare_urls(entities['urls'])
        if urls:
            print('************ URLS **********: ', urls)
            hashtags = self.prepare_hashtags(
                [hashtag['text'].lower() for hashtag in entities['hashtags']]
            )
            tweet = self.save_tweet(data, urls, hashtags)
            logger.info('Tweet Saved: %s' % tweet.text)
        return True

    def on_error(self, status):
        logger.error(status)
