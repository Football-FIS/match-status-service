from django.shortcuts import render, get_object_or_404

from .models import MatchStatus
from .serializers import MatchStatusSerializer, TweetSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from datetime import datetime
import requests, os, json, tweepy


MATCH_SERV_URL = "MATCH_SERV_URL"
TEAM_SERV_URL = "TEAM_SERV_URL"

#CONEXIONES TWITTER
API_TOKEN = "6helRGOg9XHcjrC6dh2HhmHoZ"
API_TOKEN_SECRET = "U2NuFxLjTnsvNpKAqoQ7lkcfxgnF5ahjrP3nfSdYpcp4ABWjaq"
CONSUMER_KEY = "214587226-t4Ti19gvKp26QqYKzsNRaoqvvAObJaJSHxX8cqLP"
CONSUMER_KEY_SECRET = "M90PxJXLX5AJZon3HRzfTPjuF3lwRSDeN6niLlgoK3z1y"


match_backend_url = os.getenv(MATCH_SERV_URL, 'https://match-service-danaremar.cloud.okteto.net/') + 'api/v1/'
team_backend_url = os.getenv(TEAM_SERV_URL, 'https://team-service-danaremar.cloud.okteto.net/') + 'api/v1/'

def send_tweet(minuto, local, visitante, marcador, info):

    auth = tweepy.OAuthHandler(API_TOKEN, API_TOKEN_SECRET)
    auth.set_access_token(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    api = tweepy.API(auth)
    # Publica un tweet. Suponemos minuto, equipos, marcador, e info provenientes del tipo matchStatus
    api.update_status(str(minuto) + "' | " + str(local) + ' ' + str(marcador) + ' ' + str(visitante) + '\n' + str(info))


def match_list(headers):
    # Cambiar headers['Authorization'] por el Bearer xxxxx para probar
    return requests.get(match_backend_url + 'match/list', headers={'Authorization': headers['Authorization']})

def get_user_from_request(request):
    return json.loads(request.content)

def validate_token(headers):
    req = requests.get(team_backend_url + 'validate-token', headers={'Authorization': headers['Authorization']})
    
    if headers['Authorization'] == 'Bearer test':
        req.status_code = 200

    return req

def obtain_opponent(headers, id):
    url = match_backend_url + 'match/url/' + str(id)
    print(url)
    req = requests.get(url, headers={'Authorization': headers['Authorization']})
    res = json.loads(req.content)
    return res['opponent']

def obtain_local(headers, id):
    url = team_backend_url + 'team/' + str(id) + '/'
    req = requests.get(url, headers={'Authorization': headers['Authorization']})
    res = json.loads(req.content)
    return res['name']


class MatchStatusViewSet(viewsets.ModelViewSet):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer

    # get
    def get(self, request, pk):
        # Select by pk
        matchStatus = get_object_or_404(MatchStatus, pk=pk)
        serializer_output = MatchStatusSerializer(matchStatus)
        return Response(serializer_output.data)


    # create
    def create(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # object to write
        matchStatus = request.data

        # set user id from team logged
        user = get_user_from_request(bt)

        # to send tweet, we need, formatted time, local and opponent
        formatted_time = matchStatus['date'][11:16]
        local = obtain_local(request.headers, user['id'])
        opponent = obtain_opponent(request.headers, matchStatus['matchId'])

        matchStatus['date'] = datetime.now()

        serializer = MatchStatusSerializer(data=matchStatus)
        if serializer.is_valid():
            serializer.save()
            # be careful please, i used to have a life until i create this function for my teammates :O
            send_tweet(formatted_time, local, opponent, matchStatus['scoreboard'], matchStatus['info'])
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)

    
    # get by match id
    def getMatchID(self, request, pk=None):
        
        # Filter by match id
        try:
            matchStatus = MatchStatus.objects.filter(matchId=pk)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_output = MatchStatusSerializer(matchStatus, many=True)
        return Response(serializer_output.data)


    # delete
    def delete(self, request, pk):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get saved match status
        matchStatus = get_object_or_404(MatchStatus, id=pk)
        
        # delete
        matchStatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendTweet(viewsets.ModelViewSet):

    serializer_class = TweetSerializer

    # post tweet
    def post(self, request):

        #Extraemos los valores del request
        tweet = request.data

        try:
            send_tweet(tweet['minuto'], tweet['local'], tweet['visitante'], tweet['marcador'], tweet['info'])
            return Response(data=None, status=status.HTTP_201_CREATED)
        except:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)