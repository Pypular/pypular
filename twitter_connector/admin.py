from django.contrib import admin
from twitter_connector.models import Url, Hashtag, Tweet, HashtagUrl, TweetUrl


class UrlInline(admin.TabularInline):
    model = TweetUrl
    extra = 1


class HashTagUrlInline(admin.TabularInline):
    model = HashtagUrl
    extra = 1


class TweetModelAdmin(admin.ModelAdmin):
    inlines = [UrlInline]
    list_display = ['text', 'created_at', 'retweet_count', 'favorite_count']


class UrlModelAdmin(admin.ModelAdmin):
    inlines = [HashTagUrlInline]


class HashTagUrlAdmin(admin.ModelAdmin):
    list_display = ['hashtag', 'url']


class TweetUrlAdmin(admin.ModelAdmin):
    list_display = ['tweet', 'url']


admin.site.register(Url, UrlModelAdmin)
admin.site.register(Hashtag)
admin.site.register(Tweet, TweetModelAdmin)
admin.site.register(HashtagUrl, HashTagUrlAdmin)
admin.site.register(TweetUrl, TweetUrlAdmin)
