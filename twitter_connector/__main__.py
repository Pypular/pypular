"""
Author: Denis Afonso
Description: Script for analyzing tweets based on specific topics, using the
tweepy module.
"""
from twitter_connector.utils import setup_logging
from twitter_connector.run import twitter_stream

import os
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


def main():
    setup_logging()
    try:
        twitter_stream(logger)
    except KeyboardInterrupt:
        logger.info('Exiting...')


if __name__ == '__main__':
    main()
