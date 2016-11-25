import os


def get_config(environ_key_name, default_value, convert=str):
    return convert(os.environ.get(environ_key_name, default_value))


TWITTER_CONFIG = {
    'CONSUMER_KEY': get_config('TW_CONSUMER_KEY', ''),
    'CONSUMER_SECRET': get_config('TW_CONSUMER_SECRET', ''),
    'ACCESS_TOKEN': get_config('TW_ACCESS_TOKEN', ''),
    'ACCESS_TOKEN_SECRET': get_config('TW_ACCESS_TOKEN_SECRET', ''),
}


DATABASE_URL = get_config('DATABASE_URL', 'postgres://@:5432/pypular')
