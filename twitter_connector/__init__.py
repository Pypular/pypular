import logging

logger = logging.getLogger(__name__)


def setup_logging(log_name):
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(log_name)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
