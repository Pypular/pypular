import pytest

from twitter_connector.helpers import parse_tweet, prepare_urls, prepare_hashtags
from twitter_connector.models import Url, Hashtag


@pytest.mark.parametrize('test_case', [
    # valid tweet
    {
        'filter': ['created_at', 'entities', 'favorite_count', 'id',
                   'retweet_count', 'text', 'timestamp_ms'],
        'tweet': {
            'favorite_count': 0, 'retweet_count': 0, 'text': 'text do tweet',
            'timestamp_ms': '1481054501648',
            'entities': {
                'symbols': [], 'user_mentions': [], 'hashtags': [],
                'urls': [
                    {
                        'expanded_url': 'http://ow.ly/oXTM507h7kP',
                        'display_url': 'ow.ly/oXTM507h7kP',
                        'url': 'https://t.co/kHIRMU7FBS', 'indices': [115, 138]
                    }
                ]
            },
            'id_str': '806227130937905152', 'id': 806227130937905152,
            'created_at': 'Tue Dec 06 20:01:41 +0000 2016'
        },
        'expected': {
            'retweet_count': 0, 'favorite_count': 0, 'timestamp_ms': '1481054501648',
            'text': 'text do tweet', 'id': 806227130937905152,
            'created_at': 'Tue Dec 06 20:01:41 +0000 2016',
            'entities': {
                'symbols': [], 'user_mentions': [], 'hashtags': [],
                'urls': [
                    {'expanded_url': 'http://ow.ly/oXTM507h7kP',
                     'display_url': 'ow.ly/oXTM507h7kP',
                     'url': 'https://t.co/kHIRMU7FBS', 'indices': [115, 138]}
                ]}
        },
    },
    # invalid no entities
    {
        'filter': ['created_at', 'favorite_count', 'id', 'entities', 'retweet_count',
                   'text', 'timestamp_ms'],
        'tweet': {
            'favorite_count': 0, 'retweet_count': 0, 'text': 'text do tweet',
            'timestamp_ms': '1481054501648',
            'id_str': '806227130937905152', 'id': 806227130937905152,
            'created_at': 'Tue Dec 06 20:01:41 +0000 2016'
        },
        'expected': None
    },
])
def test_parse_tweet(test_case):
    data = parse_tweet(test_case['tweet'], test_case['filter'])
    assert data == test_case['expected']


@pytest.mark.django_db
@pytest.mark.parametrize('test_case', [
    {
        'urls': [
            {
                'expanded_url': 'http://ow.ly/oXTM507h7kP',
                'display_url': 'ow.ly/oXTM507h7kP',
                'url': 'https://t.co/kHIRMU7FBS', 'indices': [115, 138]
            }
        ],
        'num_expected_urls': 1
    },
    {
        'urls': [
            {
                'expanded_url': 'https://youtu.be/X_C1RBahZq4', 'indices': [41, 64],
                'url': 'https://t.co/zXLEphJ0Vu',
                'display_url': 'youtu.be/X_C1RBahZq4'
            },
            {
                'expanded_url': 'https://youtu.be/X_C1RBahZq4', 'indices': [41, 64],
                'url': 'https://t.co/zXLEphJ0Vu',
                'display_url': 'youtu.be/X_C1RBahZq4'
            }
        ],
        'num_expected_urls': 1
    },
    {
        'urls': [
            {
                'url': 'https://t.co/Y1w8u3APPE', 'indices': [88, 111],
                'expanded_url': 'http://buff.ly/2gOxtNY', 'display_url': 'buff.ly/2gOxtNY'
            },
            {
                'url': 'https://t.co/CgOxfVwvTz', 'indices': [115, 138],
                'expanded_url': 'https://twitter.com/i/web/status/806253879121903616',
                'display_url': 'twitter.com/i/web/status/8…'
            }
        ],
        'num_expected_urls': 2
    },
    {
        'exist_url': [
            Url(
                url='https://t.co/Y1w8u3APPE',
                expanded_url='http://www.datasciencecentral.com/profiles/blogs/20-data-'
                             'science-r-python-excel-and-machine-learning-cheat-sheets?'
                             'utm_content=bufferaa9a1&utm_medium=social&utm_source=twitt'
                             'er.com&utm_campaign=buffer'
            )
        ],
        'urls': [
            {
                'url': 'https://t.co/Y1w8u3APPE', 'indices': [88, 111],
                'expanded_url': 'http://buff.ly/2gOxtNY', 'display_url': 'buff.ly/2gOxtNY'
            },
            {
                'url': 'https://t.co/CgOxfVwvTz', 'indices': [115, 138],
                'expanded_url': 'https://twitter.com/i/web/status/806253879121903616',
                'display_url': 'twitter.com/i/web/status/8…'
            }
        ],
        'num_expected_urls': 2
    },

])
def test_prepare_urls(test_case):
    save_url = []
    if 'exist_url' in test_case:
        for url in test_case['exist_url']:
            url.save()
            save_url.append(url)
    urls = prepare_urls(test_case['urls'])
    for url in save_url:
        assert url in urls

    assert len(urls) == test_case['num_expected_urls']


@pytest.mark.django_db
@pytest.mark.parametrize('test_case', [
    {
        'hashtags': ['test1', 'teste2'],
        'num_expected_hashtags': 2
    },
    {
        'hashtags': ['test1', 'test1'],
        'num_expected_hashtags': 1
    },
    {
        'hashtags': [],
        'num_expected_hashtags': 0
    },
    {
        'exist_hashtag': 'test1',
        'hashtags': ['test4', 'test1'],
        'num_expected_hashtags': 2
    },
])
def test_prepare_hashtags(test_case):
    if 'exist_hashtag' in test_case:
        hashtag = Hashtag(hashtag=test_case['exist_hashtag'])
        hashtag.save()
    hashtags = prepare_hashtags(test_case['hashtags'])
    if 'exist_hashtag' in test_case:
        assert hashtag in hashtags
    assert len(hashtags) == test_case['num_expected_hashtags']
