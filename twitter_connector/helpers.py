import logging
import requests

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from twitter_connector.models import Url, Hashtag, Tweet

logger = logging.getLogger(__name__)


def get_expanded_url(url, max_retries=3):
    # todo: add error handling
    for retry in range(max_retries):
        try:
            req = requests.head(url, allow_redirects=True, timeout=10)
        except:
            logger.error('Unable to connect to url: %s', url)
            logger.info('Retrying the connection. Attempt %s out of %s' % (
                retry + 1, max_retries))
        else:
            return req.url or 'invalid_url'  # TODO: need some verification
    return url


def parse_tweet(tweet, filters):
    data = {}
    for filter in filters:
        try:
            data[filter] = tweet[filter]
        except KeyError:
            logger.error('No %s found on tweet' % filter)
            if filter == 'created_at':
                data[filter] = timezone.now()
                logger.info('Using current datetime %s.' % data[filter])
            else:
                logger.error('Exiting so we can catch and fix the error')
                data = None
                break
    return data


def prepare_urls(urls):
    urls_to_save = {}
    for url in urls:
        if url['url']:
            exp_url = get_expanded_url(url['expanded_url'])
            if exp_url not in urls_to_save.keys():
                try:
                    new_url = Url.objects.get(expanded_url=exp_url)
                    new_url.modified_at = timezone.now()
                    urls_to_save[exp_url] = new_url
                except ObjectDoesNotExist:
                    try:
                        Url.objects.get(url=url['expanded_url'])
                        logger.warn(
                            'Found matching url but different expanded_url. Skipping...'
                        )
                    except ObjectDoesNotExist:
                        new_url = Url()
                        new_url.url = url['url']
                        new_url.expanded_url = exp_url
                        urls_to_save[exp_url] = new_url

    return list(urls_to_save.values())


def prepare_hashtags(hashtags):
    hashtags = set(hashtags)
    hashtag_list = []
    for tag in hashtags:
        if tag not in hashtag_list:
            try:
                new_tag = Hashtag.objects.get(hashtag=tag)
            except ObjectDoesNotExist:
                new_tag = Hashtag()
                new_tag.hashtag = tag

            hashtag_list.append(new_tag)

    return hashtag_list


def save_tweet(tweet_data):
    urls = prepare_urls(tweet_data['entities']['urls'])
    logger.info('************ URLS **********: {0}'.format(urls))
    hashtags = prepare_hashtags(
        [hashtag['text'].lower() for hashtag in tweet_data['entities']['hashtags']]
    )
    logger.info('************ Hashtags **********: {0}'.format(hashtags))
    try:
        tweet = Tweet.objects.get(pk=tweet_data['id'])
        _urls = [url.url.expanded_url for url in list(tweet.tweeturl_set.all())]
        for url in urls:
            if url.expanded_url in _urls:
                urls.remove(url)
    except ObjectDoesNotExist:
        created_at = timezone.datetime.strptime(
            tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y'
        )
        tweet = Tweet(
            id=tweet_data['id'], created_at=created_at, text=tweet_data['text'],
            timestamp_ms=tweet_data['timestamp_ms'], retweet_count=tweet_data['retweet_count'],
            favorite_count=tweet_data['favorite_count']
        )

    tweet.save_tweet(urls=urls, hashtags=hashtags)
    logger.info('Tweet Saved: %s' % tweet.text)
    return tweet
