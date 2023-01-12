from rest_framework import serializers
from .models import MatchStatus, Tweet

class MatchStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model =  MatchStatus
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Tweet
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }