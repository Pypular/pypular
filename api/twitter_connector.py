"""
Author: Denis Afonso
Description: Script for analyzing tweets based on specific topics, using the
tweepy module.
"""
import logging
import tweepy

from api.utils import setup_logging, load_config
from api.listeners import DBListener

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


def main():
    setup_logging(logger)

    # TODO: Add exception handling
    config = load_config(os.path.join(BASE_DIR, 'conf/api.yaml'), logger)
    twitter_conf = config['twitter']

    CONSUMER_KEY = twitter_conf['CONSUMER_KEY']
    CONSUMER_SECRET = twitter_conf['CONSUMER_SECRET']
    ACCESS_TOKEN = twitter_conf['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_conf['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    listener = DBListener('pypular')
    stream = tweepy.Stream(auth, listener, retry_count=50)
    logger.info('Initializing Twitter Streaming Listener...')

    try:
        stream.filter(track=[
            'python programming', 'python tutorial', 'python language',
            'python code', 'python coding', 'python API',
            'python data', 'python machine', 'python hack',
            'python script', 'python keynote', 'python server',
            'python application', 'python django', 'python web',
            'django programming', 'django web', 'django app',
            'django tutorial', 'python flask', 'flask app',
            'flask tutorial', 'flask web', 'scipy', 'numpy'
        ])
    except AttributeError:
        logger.error('Error!', exc_info=True)
        main()

if __name__ == '__main__':
    main()
