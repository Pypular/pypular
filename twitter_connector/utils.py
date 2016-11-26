import logging
import requests


logger = logging.getLogger(__name__)


def get_expanded_url(url, max_retries=3):
    # todo: add error handling
    for retry in range(max_retries):
        try:
            req = requests.head(url, allow_redirects=True, timeout=10)
        except:
            logger.error('Unable to connect to url: %s', url)
            logger.info('Retrying the connection. Attempt %s out of %s' % (
                retry + 1, max_retries))
        else:
            return req.url or 'invalid_url'  # TODO: need some verification
    return url
