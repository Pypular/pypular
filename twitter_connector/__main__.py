#!/usr/bin/env python
from twitter_connector.utils import setup_logging

import os
import logging

from twitter_connector import setup_logging
from twitter_connector.run import twitter_stream


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    setup_logging('twitter_connector.log')
    try:
        twitter_stream(logger)
    except KeyboardInterrupt:
        logger.info('Exiting...')

    os.environ.setdefault("SIMPLE_SETTINGS", "twitter_connector.settings")