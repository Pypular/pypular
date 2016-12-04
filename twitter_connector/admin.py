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
    search_fields = ['text']
    list_filter = ['created_at']


class UrlModelAdmin(admin.ModelAdmin):
    inlines = [HashTagUrlInline]
    list_display = ['url', 'expanded_url']
    search_fields = ['url', 'expanded_url']


class HashTagUrlAdmin(admin.ModelAdmin):
    list_display = ['hashtag', 'url']
    search_fields = ['hashtag', 'url']


class TweetUrlAdmin(admin.ModelAdmin):
    list_display = ['tweet', 'url']
    search_fields = ['tweet', 'url']


class HastagModelAdmin(admin.ModelAdmin):
    search_fields = ['hashtag']

admin.site.register(Url, UrlModelAdmin)
admin.site.register(Hashtag, HastagModelAdmin)
admin.site.register(Tweet, TweetModelAdmin)
admin.site.register(HashtagUrl, HashTagUrlAdmin)
admin.site.register(TweetUrl, TweetUrlAdmin)
