# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Hashtags(models.Model):
    id = models.BigIntegerField(unique=True)
    hashtag = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'hashtags'
        unique_together = (('id', 'hashtag'),)


class HashtagsUrls(models.Model):
    urls = models.ForeignKey('Urls', models.DO_NOTHING)
    hashtags = models.ForeignKey(Hashtags, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hashtags_urls'
        unique_together = (('urls', 'hashtags'),)


class Tweets(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    timestamp_ms = models.BigIntegerField(blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    retweet_count = models.IntegerField(blank=True, null=True)
    favorite_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tweets'


class TweetsUrls(models.Model):
    tweets = models.ForeignKey(Tweets, models.DO_NOTHING)
    urls = models.ForeignKey('Urls', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tweets_urls'
        unique_together = (('tweets', 'urls'),)


class Urls(models.Model):
    id = models.BigIntegerField(unique=True)
    url = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'urls'
        unique_together = (('id', 'url'),)
