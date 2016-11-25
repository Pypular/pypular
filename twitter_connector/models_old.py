import logging

from datetime import datetime
from decouple import config
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, BigInteger, Text, ForeignKey, Table
)
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)
Base = declarative_base()


def setup_db():
    logger.info('Opening connection with DB')
    engine = create_engine(config('DATABASE'), echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


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
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    urls = relationship('Url', secondary=tweets_urls, back_populates='tweets')

    def __repr__(self):
        return "<Tweet(text='%s')>" % self.text


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(BigInteger, primary_key=True, unique=True)
    hashtag = Column(String(100), unique=True, primary_key=True)
    urls = relationship('Url', secondary=hashtags_urls, back_populates='hashtags')

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
    tweets = relationship('Tweet', secondary=tweets_urls, back_populates='urls')
    hashtags = relationship('Hashtag', secondary=hashtags_urls, back_populates='urls')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Url(url='%s')>" % self.url
