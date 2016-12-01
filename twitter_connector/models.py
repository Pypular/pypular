from datetime import datetime
from django.db import models


class Url(models.Model):

    url = models.TextField('url', unique=True, null=False)
    expanded_url = models.TextField('expanded_url')
    created_at = models.DateTimeField('created_at', default=datetime.utcnow)
    modified_at = models.DateTimeField('modified_at', default=datetime.utcnow)
    # tweet = relationship('Tweet', secondary=tweets_urls, back_populates='urls')
    # hashtag = relationship('Hashtag', secondary=hashtags_urls, back_populates='urls')

    class Meta:
        db_table = 'url'
        verbose_name = 'url'
        verbose_name_plural = 'urls'
        unique_together = (('id', 'url'),)

    def __str__(self):
        return self.url

    def __repr__(self):
        return "<Url(url='%s')>" % self.url


class Tweet(models.Model):

    id = models.BigIntegerField(primary_key=True, unique=True)
    created_at = models.DateTimeField('created_at')
    timestamp_ms = models.BigIntegerField('timestamp_ms')
    text = models.CharField('text', max_length=150)
    retweet_count = models.IntegerField('retweet_count')
    favorite_count = models.IntegerField('favorite_count')
    urls = models.ManyToManyField('Url', verbose_name='urls', through='TweetUrl')

    class Meta:
        db_table = 'tweet'
        verbose_name = 'tweet'
        verbose_name_plural = 'tweets'

    def __str__(self):
        return self.text[:20] + '...'

    def __repr__(self):
        return "<Tweet(text='%s')>" % self.text


class Hashtag(models.Model):

    hashtag = models.CharField('hashtag', max_length=100, unique=True)
    urls = models.ManyToManyField('Url', verbose_name='urls', through='HashtagUrl')

    class Meta:
        db_table = 'hashtag'
        verbose_name = 'hashtag'
        verbose_name_plural = 'hashtags'

    def __str__(self):
        return self.hashtag

    def __repr__(self):
        return "<Hashtag(hashtag='%s')>" % self.hashtag


class HashtagUrl(models.Model):

    url = models.ForeignKey('Url')
    hashtag = models.ForeignKey('Hashtag')

    class Meta:
        db_table = 'hashtag_url'
        verbose_name = 'hashtagurl'
        verbose_name_plural = 'hashtagurls'
        unique_together = (('url', 'hashtag'),)


class TweetUrl(models.Model):

    tweet = models.ForeignKey('Tweet')
    url = models.ForeignKey('Url')

    class Meta:
        db_table = 'tweet_url'
        verbose_name = 'tweeturl'
        verbose_name_plural = 'tweeturls'
        unique_together = (('tweet', 'url'),)
