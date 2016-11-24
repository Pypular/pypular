import tweepy

from decouple import config
from twitter_connector.listeners import DBListener


def twitter_stream(logger):
    CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET')
    ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    listener = DBListener('pypular')
    stream = tweepy.Stream(auth, listener, retry_count=50)
    logger.info('Initializing Twitter Streaming Listener...')
    stream.filter(track=[
        'python programming', 'python tutorial', 'python language',
        'python code', 'python coding', 'python API',
        'python data', 'python machine', 'python hack',
        'python script', 'python keynote', 'python server',
        'python application', 'python django', 'python web',
        'django programming', 'django web', 'django app',
        'django tutorial', 'python flask', 'flask app',
        'flask tutorial', 'flask web', 'scipy', 'numpy'
    ])
