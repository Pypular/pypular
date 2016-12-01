from datetime import datetime
from django.db import models, transaction


class Url(models.Model):

    url = models.TextField('url', unique=True, null=False)
    expanded_url = models.TextField('expanded_url')
    created_at = models.DateTimeField('created_at', default=datetime.utcnow)
    modified_at = models.DateTimeField('modified_at', default=datetime.utcnow)

    class Meta:
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
        verbose_name = 'tweet'
        verbose_name_plural = 'tweets'

    def __str__(self):
        return self.text[:20] + '...'

    def __repr__(self):
        return "<Tweet(text='%s')>" % self.text

    def save(self, *args, **kwargs):
        if not args:
            self.save()
        else:
            super().save()
            try:
                urls, hashtags = kwargs['urls'], kwargs['hashtags']
                 # for url in urls:
                #     tweet_url = TweetUrl()
                #     tweet_url.tweet = tweet
                #     tweet_url.url = url
                #     tweet_url.save()
                #     tweet.tweeturl_set.add(tweet_url)
                # def save_urls(self, hashtags, urls):
                #     for url in urls:
                #         url.save()
                #         for hashtag in hashtags:
                #             if not url.hashtagurl_set.all().filter(hashtag=hashtag):
                #                 hashtag_url = HashtagUrl()
                #                 hashtag_url.hashtag = hashtag
                #                 hashtag_url.url = url
                #                 hashtag_url.save()
                #                 url.hashtagurl_set.add(hashtag_url)
                #     return urls
            except:
                transaction.rollback()

        print("salva")
        # save url
        # save hashtag
        # save tweet
        pass


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
