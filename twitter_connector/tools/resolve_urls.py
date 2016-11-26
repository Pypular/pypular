"""
Author: Denis Afonso
Description: Script used to resolve/expand shortened urls and replace the
corresponding entries in the DB.
"""
import logging

from datetime import datetime
from twitter_connector import setup_logging
from twitter_connector.models import Url, setup_db as session
from twitter_connector.utils import get_expanded_url

logger = logging.getLogger(__name__)


def get_urls():
    urls = session.query(Url).all()
    return urls


def get_url(url):
    return session.query(Url).filter_by(expanded_url=url).first()


def update_url(url, expanded_url):
    original_url = get_url(expanded_url)
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

if __name__ == '__main__':
    setup_logging('resolve_urls.log')
    urls = get_urls()
    for url in urls:
        expanded_url = get_expanded_url(url.url)
        if url.expanded_url != expanded_url:
            logger.warn('Different: %s and %s' % (url.expanded_url, expanded_url))
            update_url(url, expanded_url)
        else:
            logger.info('Match: %s and %s' % (url.expanded_url, expanded_url))
            short_url = get_url(expanded_url)
            if url.id != short_url.id:
                logger.warn('IDs mismatch: %s and %s', url.id, short_url.id)
                update_url(url, expanded_url)
