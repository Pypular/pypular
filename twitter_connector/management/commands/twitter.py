import django
django.setup()
from django.core.management.base import BaseCommand

import os
import logging

from twitter_connector import setup_logging
from twitter_connector.run import twitter_stream


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        setup_logging('twitter_connector.log')
        try:
            twitter_stream(logger)
        except KeyboardInterrupt:
            logger.info('Exiting...')

if __name__ == '__main__':
    setup_logging('twitter_connector.log')
    try:
        twitter_stream(logger)
    except KeyboardInterrupt:
        logger.info('Exiting...')