from django.shortcuts import get_object_or_404

from .models import MatchStatus
from .serializers import MatchStatusSerializer
from rest_framework import viewsets, status

from rest_framework.response import Response
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json


OPEN_WEATHER_KEY = "OPEN_WEATHER_KEY"
DEFAULT_OPEN_WEATHER_KEY = 'b8de83b3476d58590a4fbf3661f4dabe'
TEAM_SERV_URL = "TEAM_SERV_URL"

team_backend_url = os.getenv(TEAM_SERV_URL, 'http://localhost:8000/') + 'api/v1/'

def validate_token(headers):
    return requests.get(team_backend_url + 'validate-token', headers={'Authorization': headers['Authorization']})

def get_user_from_request(request):
    return json.loads(request.content)

def get_weather(city):
    open_weather_key = os.environ.get(OPEN_WEATHER_KEY, DEFAULT_OPEN_WEATHER_KEY)
    api = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key).json()
    if api['cod'] == '404':
        return ''
    celsius = api['main']['temp'] - 273.15
    return api['weather'][0]['description'] + ' - Temperatura: %.2f ' %celsius

class MatchStatusViewSet(viewsets.ModelViewSet):
    #queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer

    # list
    def list(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # list all matches from team
        # queryset = Match.objects.all()

        # list only from user
        user = get_user_from_request(bt)
        queryset = MatchStatus.objects.filter(user_id=user['id'])
        serializer_class = MatchStatusSerializer(queryset, many=True)
        return Response(serializer_class.data)
        
    # get
    def get(self, request, pk=None):
        match = get_object_or_404(MatchStatus, pk=pk)
        serializer_output = MatchStatusSerializer(match)
        return Response(serializer_output.data)

    # create
    def create(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # object to write
        match = request.data

        # WeatherAPI
        match['weather'] = get_weather(request.data['city'])
            
        # Team service
        user = get_user_from_request(bt)
        match['user_id'] = user['id']

        serializer = MatchStatusSerializer(data=match)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


    # update
    def update(self, request, pk):

        # get saved match
        match = get_object_or_404(MatchStatus, pk=pk)

        # check permissions
        bt = validate_token(request.headers)
        user = get_user_from_request(bt)
        if(bt.status_code!=200 and match.user_id == user['id']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # object to write
        new_match = request.data

        # WeatherAPI
        new_match['weather'] = get_weather(request.data['city'])
            
        # Team service
        user = get_user_from_request(bt)
        new_match['user_id'] = user['id']

        # update if valid
        serializer = MatchStatusSerializer(data=new_match)
        serializer.is_valid()
        serializer.update(match, new_match)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete
    def delete(self, request, pk):

        # get saved match
        match = get_object_or_404(MatchStatus, pk=pk)

        # check permissions
        bt = validate_token(request.headers)
        user = get_user_from_request(bt)
        if(bt.status_code!=200 and match.user_id == user['id']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # delete
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)