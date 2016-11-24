"""
Author: Denis Afonso
Description: Script for analyzing tweets based on specific topics, using the
tweepy module.
"""

import os
import logging

from twitter_connector.utils import setup_logging
from twitter_connector.run import twitter_stream


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    setup_logging()
    try:
        twitter_stream(logger)
    except KeyboardInterrupt:
        logger.info('Exiting...')
