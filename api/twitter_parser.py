"""
Author: Denis Afonso
Description: Parse tweets in json format and feed a database with specific
fields for each tweet.
"""

import logging
import json
from pprint import pprint
from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.twitter_connector import setup_logging

logger = logging.getLogger(__name__)
Base = declarative_base()

def read_tweet(file_name):
    with open(file_name, 'r') as file:
        while file:
            tweet = file.readline()
            if tweet:
                yield json.loads(tweet)

def parse_tweet(tweet, *args):
    data = {}
    for arg in args:
        data[arg] = tweet[arg]
    return data

def setup_db(db_name):
    logger.info('Opening connection with DB %s' % db_name)
    engine = create_engine('postgresql://dra@:5432/pypular',
                           echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    timestamp_ms = Column(BigInteger)
    text = Column(String(255))
    url = Column(String(255))
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)




def main():
    setup_logging()
    session = setup_db('pypular')
    filter = ['created_at', 'entities', 'favorite_count', 'id',
              'retweet_count', 'text', 'timestamp_ms']
    tweets = read_tweet('tweets.json')
    for tweet in tweets:
        data = parse_tweet(tweet, *filter)
        print(data)
        urls = data['entities']['urls']
        if urls:
            new_tweet = Tweet(id = data['id'], created_at = data['created_at'],
                          timestamp_ms = data['timestamp_ms'], text = data[
                'text'], url = urls[0]['expanded_url'], retweet_count = data[
                    'retweet_count'], favorite_count = data['favorite_count'])
            print(new_tweet.created_at, new_tweet.url)
            session.add(new_tweet)
    session.commit()
            #t = session.query(Tweet).first()
        #break
        #for url in urls:
        #    pprint(url['expanded_url'])


if __name__ == '__main__':
    main()