from django.conf import settings

from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH 
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank = True, required = False)

    def validate_action(self, value):
        action = value.lower().strip()
        if not action in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This action is not valid.")
        return action 

class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Tweet
        fields = ['id','content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Tweet is too long")
        
        return value

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    og_tweet = TweetCreateSerializer(source ="parent", read_only = True)
    
    class Meta:
        model = Tweet
        fields = ['id','content', 'likes', 'is_retweet', 'og_tweet']

    def get_likes(self, obj):
        return obj.likes.count()
    
    