import logging
import yaml


def setup_logging(logger):
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('twitter_connector.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def load_config(config_file, logger):
    logger.info('Loading configuration file')
    try:
        with open(config_file, 'r') as config_file:
            config = yaml.load(config_file)
    except IOError:
        logger.error('Unable to load the config file', exc_info=True)
    else:
        logger.info('Configuration file loaded')
        return config
