import logging
import yaml
import requests


logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('twitter_connector.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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


def load_config(config_file):
    logger.info('Loading configuration file')
    try:
        with open(config_file, 'r') as config_file:
            config = yaml.load(config_file)
    except IOError:
        logger.error('Unable to load the config file', exc_info=True)
    else:
        logger.info('Configuration file loaded')
        return config
