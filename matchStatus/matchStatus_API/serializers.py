from rest_framework import serializers
from .models import MatchStatus

class MatchStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model =  MatchStatus
        fields = '__all__'