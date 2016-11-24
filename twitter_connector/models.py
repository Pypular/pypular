import logging

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, BigInteger, Text, ForeignKey, Table
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
Base = declarative_base()


def setup_db(db_name):
    logger.info('Opening connection with DB %s' % db_name)
    engine = create_engine('postgresql://:5432/' + db_name, echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()

# tweets_hashtags = Table('tweets_hashtags', Base.metadata,
#     Column('tweets_id', BigInteger, ForeignKey('tweets.id'), primary_key=True),
#     Column('hashtags_id', BigInteger, ForeignKey('hashtags.id'), primary_key=True)
# )

tweets_urls = Table(
    'tweets_urls', Base.metadata,
    Column('tweets_id', BigInteger, ForeignKey('tweets.id'), primary_key=True),
    Column('urls_id', BigInteger, ForeignKey('urls.id'), primary_key=True)
)

hashtags_urls = Table(
    'hashtags_urls', Base.metadata,
    Column('urls_id', BigInteger, ForeignKey('urls.id'), primary_key=True),
    Column('hashtags_id', BigInteger, ForeignKey('hashtags.id'), primary_key=True)
)


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True, unique=True)
    created_at = Column(DateTime)
    timestamp_ms = Column(BigInteger)
    text = Column(String(255))
    # url = Column(String(255))
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    # hashtags = relationship('Hashtag', secondary=tweets_hashtags,
    #                         back_populates='tweets')
    urls = relationship('Url', secondary=tweets_urls,
                        back_populates='tweets')

    def __repr__(self):
        return "<Tweet(text='%s')>" % self.text
        # return "<Tweet(created_at='%s', text='%s', retweet_count='%s, " \
        #        "favorite_count='%s', urls='%s', timestamp_ms='%s')>" \
        #        % (self.created_at, self.text, self.retweet_count,
        #           self.favorite_count, self.urls, self.timestamp_ms)


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(BigInteger, primary_key=True, unique=True)
    hashtag = Column(String(100), unique=True, primary_key=True)
    # tweet_id = Column(BigInteger, ForeignKey('tweets.id'), primary_key=True)
    # tweets = relationship('Tweet', secondary=tweets_hashtags,
    #                       back_populates='hashtags')
    urls = relationship('Url', secondary=hashtags_urls,
                        back_populates='hashtags')

    def __init__(self, hashtag):
        self.hashtag = hashtag

    def __repr__(self):
        return "<Hashtag(hashtag='%s')>" % self.hashtag


class Url(Base):
    __tablename__ = 'urls'

    id = Column(BigInteger, primary_key=True, unique=True)
    url = Column(Text, unique=True, primary_key=True)
    expanded_url = Column(Text, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)
    tweets = relationship('Tweet', secondary=tweets_urls,
                          back_populates='urls')
    hashtags = relationship('Hashtag', secondary=hashtags_urls,
                            back_populates='urls')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Url(url='%s')>" % self.url
