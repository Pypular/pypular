"""
Author: Denis Afonso
Description: Script for analyzing tweets based on specific topics, using the
tweepy module.
"""

import logging
import yaml
import tweepy
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    BigInteger, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


logger = logging.getLogger(__name__)
Base = declarative_base()


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


class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


class FileListener(tweepy.StreamListener):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        logger.info('Opening file %s' % self.file_name)
        self.file = open(self.file_name, 'w')

    # def __enter__(self):
    #     logger.info('Opening file %s' % self.file_name)
    #     self.file = open(self.file_name, 'wb')
    #     return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        logger.info('Closing file %s' % self.file_name)

    def on_data(self, data):
        self.file.write(data)
        return True

    def on_error(self, status):
        logger.error(status, exec_info=True)


tweet_hashtags = Table('tweet_hashtags', Base.metadata,
    Column('tweets_id', BigInteger, ForeignKey('tweets.id'), primary_key=True),
    Column('hashtags_id', Integer, ForeignKey('hashtags.id'), primary_key=True)
)


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True, unique=True)
    created_at = Column(DateTime)
    timestamp_ms = Column(BigInteger)
    text = Column(String(255))
    url = Column(String(255))
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    hashtags = relationship('Hashtag', secondary=tweet_hashtags,
                            back_populates='tweets')


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True, unique=True)
    hashtag = Column(String(100), unique=True, primary_key=True)
    #tweet_id = Column(BigInteger, ForeignKey('tweets.id'), primary_key=True)
    tweets = relationship('Tweet', secondary=tweet_hashtags,
                          back_populates='hashtags')

    def __init__(self, hashtag):
        self.hashtag = hashtag


class DBListener(tweepy.StreamListener):

    def __init__(self, db_name):
        super().__init__()
        self.filter = ['created_at', 'entities', 'favorite_count', 'id',
              'retweet_count', 'text', 'timestamp_ms']
        self.db_name = db_name
        self.session = self.setup_db()

    def setup_db(self):
        logger.info('Opening connection with DB %s' % self.db_name)
        engine = create_engine('postgresql://dra@:5432/pypular',
                               echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        return Session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        logger.info('Closing connection with DB %s' % self.db_name)

    def parse_tweet(self, tweet, *args):
        data = {}
        for arg in args:
            data[arg] = tweet[arg]
        return data

    def get_hashtags(self, entities):
        hashtags =[]
        for hashtag in entities['hashtags']:
            tag = self.session.query(Hashtag).filter_by(
                    hashtag=hashtag['text']).first()
            if tag:
                hashtags.append(tag)
            else:
                hashtags.append(Hashtag(hashtag['text']))
        return hashtags


    def on_data(self, raw_data):
        json_tweet = json.loads(raw_data)
        data = self.parse_tweet(json_tweet, *self.filter)
        urls = data['entities']['urls']
        if urls:
            tweet = Tweet(id = data['id'], created_at = data['created_at'],
                          timestamp_ms = data['timestamp_ms'], text = data[
                'text'], url = urls[0]['expanded_url'], retweet_count = data[
                    'retweet_count'], favorite_count = data['favorite_count'])
            hashtags = self.get_hashtags(data['entities'])
            print('hashtags: ', hashtags)
            tweet.hashtags = hashtags
            logger.info('Saving Tweet: %s' % tweet.text)
            self.session.add(tweet)
            self.session.commit()
        return True

    def on_error(self, status):
        logger.error(status, exec_info=True)


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('twitter_connector.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():

    setup_logging()

    # TODO: Add exception handling
    config = load_config('conf/api.yaml')
    twitter_conf = config['twitter']

    CONSUMER_KEY = twitter_conf['CONSUMER_KEY']
    CONSUMER_SECRET = twitter_conf['CONSUMER_SECRET']
    ACCESS_TOKEN = twitter_conf['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_conf['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # listener = StdOutListener()
    listener = DBListener('tweets.json')
    stream = tweepy.Stream(auth, listener, retry_count=50)
    logger.info('Initializing Twitter Streaming Listener...')

    try:

        stream.filter(track=['python programming', 'python tutorial', 'python language',
                         'python code', 'python coding', 'python API',
                         'python data', 'python machine', 'python hack',
                         'python script', 'python keynote', 'python server',
                         'python application'])
    except AttributeError:
        logger.error('Error!', exc_info=True)
        main()

if __name__ == '__main__':
    main()
