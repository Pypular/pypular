import json
import logging

import tweepy

from twitter_connector import helpers

logger = logging.getLogger(__name__)


class DBListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.filter = ['created_at', 'entities', 'favorite_count', 'id',
                       'retweet_count', 'text', 'timestamp_ms']

    def on_data(self, raw_data):
        try:
            json_tweet = json.loads(raw_data)
            if 'entities' not in json_tweet:
                return True
        except TypeError:
            logger.error('Error reading tweet:', exc_info=True)
            return True
        tweet_data = helpers.parse_tweet(json_tweet, self.filter)
        if not tweet_data:
            return True

        if tweet_data['entities']['urls']:
            try:
                helpers.save_tweet(tweet_data)
            except:
                logger.error('Error on save tweet: ', exc_info=True)

        return True

    def on_error(self, status):
        logger.error(status)
