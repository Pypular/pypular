from django.utils import timezone
from django.db import models, transaction


class Url(models.Model):

    url = models.TextField('url', null=False)
    expanded_url = models.TextField('expanded_url', unique=True)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    modified_at = models.DateTimeField('modified_at', default=timezone.now)

    class Meta:
        verbose_name = 'url'
        verbose_name_plural = 'urls'
        unique_together = (('id', 'expanded_url'),)

    def __str__(self):
        return self.expanded_url

    def __repr__(self):
        return "<Url(url='%s')>" % self.expanded_url


class Tweet(models.Model):

    id = models.BigIntegerField(primary_key=True, unique=True)
    created_at = models.DateTimeField('created_at')
    timestamp_ms = models.BigIntegerField('timestamp_ms')
    text = models.CharField('text', max_length=150)
    retweet_count = models.IntegerField('retweet_count')
    favorite_count = models.IntegerField('favorite_count')
    urls = models.ManyToManyField('Url', verbose_name='urls', through='TweetUrl')

    class Meta:
        verbose_name = 'tweet'
        verbose_name_plural = 'tweets'

    def __str__(self):
        return self.text[:20] + '...'

    def __repr__(self):
        return "<Tweet(text='%s')>" % self.text

    @transaction.atomic
    def save_tweet(self, *args, **kwargs):
        self.save()
        urls, hashtags = kwargs['urls'], kwargs['hashtags']
        for url in urls:
            url.save()
            tweet_url = TweetUrl()
            tweet_url.tweet = self
            tweet_url.url = url
            tweet_url.save()
            for hashtag in hashtags:
                hashtag.save()
                if not url.hashtagurl_set.all().filter(hashtag=hashtag):
                    hashtag_url = HashtagUrl()
                    hashtag_url.hashtag = hashtag
                    hashtag_url.url = url
                    hashtag_url.save()


class Hashtag(models.Model):

    hashtag = models.CharField('hashtag', max_length=100, unique=True)
    urls = models.ManyToManyField('Url', verbose_name='urls', through='HashtagUrl')

    class Meta:
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
        verbose_name = 'hashtagurl'
        verbose_name_plural = 'hashtagurls'
        unique_together = (('url', 'hashtag'),)


class TweetUrl(models.Model):

    tweet = models.ForeignKey('Tweet')
    url = models.ForeignKey('Url')

    class Meta:
        verbose_name = 'tweeturl'
        verbose_name_plural = 'tweeturls'
        unique_together = (('tweet', 'url'),)
