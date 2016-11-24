"""
Author: Denis Afonso
Description: Script used to resolve/expand shortened urls and replace the
corresponding entries in the DB.
"""

import logging
from datetime import datetime
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print('sys.path: ', sys.path)
from twitter_connector.models import Url
from twitter_connector.utils import get_expanded_url

logger = logging.getLogger(__name__)


def setup_db(db_name):
    logger.info('Opening connection with DB %s' % db_name)
    engine = create_engine('postgresql://dra@:5432/' + db_name,
                           echo=True)
    Session = sessionmaker(bind=engine)

    return Session()


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('resolve_urls.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_urls(session):
    urls = session.query(Url).all()
    return urls


def get_url(session, url):
    return session.query(Url).filter_by(expanded_url=url).first()


def update_url(session, url, expanded_url):
    original_url = get_url(session, expanded_url)
    if original_url:
        logger.warn('Original Url already exists: %s' % original_url.url)
        for hashtag in url.hashtags:
            if hashtag not in original_url.hashtags:
                original_url.hashtags.append(hashtag)
        for tweet in url.tweets:
            if tweet not in original_url.tweets:
                original_url.tweets.append(tweet)
        if not original_url.created_at:
            if original_url.tweets[0].created_at:
                original_url.created_at = original_url.tweets[0].created_at
            else:
                original_url.created_at = datetime.utcnow()
        if not original_url.modified_at:
            original_url.modified_at = datetime.utcnow()
        session.delete(url)
    else:
        logger.info('Original Url does not exist. Updating Url.')
        url.expanded_url = expanded_url
        if not url.created_at:
            if url.tweets[0].created_at:
                url.created_at = url.tweets[0].created_at
            else:
                url.created_at = datetime.utcnow()
        if not url.modified_at:
            url.modified_at = datetime.utcnow()
    session.commit()


def main():
    setup_logging()
    session = setup_db('pypular')
    urls = get_urls(session)
    for url in urls:
        expanded_url = get_expanded_url(url.url)
        if url.expanded_url != expanded_url:
            logger.warn('Different: %s and %s' % (url.expanded_url, expanded_url))
            update_url(session, url, expanded_url)
        else:
            logger.info('Match: %s and %s' % (url.expanded_url, expanded_url))
            short_url = get_url(session, expanded_url)
            if url.id != short_url.id:
                logger.warn('IDs mismatch: %s and %s', url.id, short_url.id)
                update_url(session, url, expanded_url)


if __name__ == '__main__':
    main()
