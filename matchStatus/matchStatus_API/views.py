from django.shortcuts import render, get_object_or_404

from .models import MatchStatus
from .serializers import MatchStatusSerializer, TweetSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import requests, os, json, tweepy


MATCH_SERV_URL = "MATCH_SERV_URL"
TEAM_SERV_URL = "TEAM_SERV_URL"

#CONEXIONES TWITTER
API_TOKEN = "6helRGOg9XHcjrC6dh2HhmHoZ"
API_TOKEN_SECRET = "U2NuFxLjTnsvNpKAqoQ7lkcfxgnF5ahjrP3nfSdYpcp4ABWjaq"
CONSUMER_KEY = "214587226-t4Ti19gvKp26QqYKzsNRaoqvvAObJaJSHxX8cqLP"
CONSUMER_KEY_SECRET = "M90PxJXLX5AJZon3HRzfTPjuF3lwRSDeN6niLlgoK3z1y"


#No tenemos que crear validate token, debido a que si llega a nuestra api, es porque debes estar logueado (match-service nos controla el acceso por team-service)
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
    return requests.get(team_backend_url + 'validate-token', headers={'Authorization': headers['Authorization']})


class MatchStatusViewSet(viewsets.ModelViewSet):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer


    def list(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
         # list only from user
        user = get_user_from_request(bt)
        queryset = MatchStatus.objects.filter(user_id=user['id'])

        # AUTENTICACION A TRAVÉS DE MATCH
        # # extract match list
        # bt = match_list(request.headers)
        # if(bt.status_code!=200):
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # # get match list info
        # match = get_user_from_request(bt)

        # try:
        #     # list all matchesStatus with user id coincidence
        #     queryset = MatchStatus.objects.filter(user_id=match['user_id'])
        # except:
        #     return Response(status=status.HTTP_204_NO_CONTENT)



        serializer_class = MatchStatusSerializer(queryset, many=True)
        return Response(serializer_class.data)


    # create
    def create(self, request):

        # object to write
        matchStatus = request.data

        serializer = MatchStatusSerializer(data=matchStatus)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)

    
    # get
    def get(self, request, pk=None):
        matchStatus = get_object_or_404(MatchStatus, pk=pk)
        serializer_output = MatchStatusSerializer(matchStatus)
        return Response(serializer_output.data)


    # update
    def update(self, request, pk):

        # object to write
        new_match_status = request.data

        # get saved matchStatus
        # in swagger you must insert manually id:xxxx
        matchStatus = get_object_or_404(MatchStatus, id=pk)

        # update if valid
        serializer = MatchStatusSerializer(data=new_match_status)
        serializer.is_valid()
        serializer.update(matchStatus, new_match_status)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # delete
    def delete(self, pk):

        # get saved match status
        match = get_object_or_404(MatchStatus, pk=pk)
        
        # delete
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendTweet(viewsets.ModelViewSet):

    serializer_class = TweetSerializer

    # get
    def post(self, request):

        #Extraemos los valores del request
        tweet = request.data

        try:
            send_tweet(tweet['minuto'], tweet['local'], tweet['visitante'], tweet['marcador'], tweet['info'])
            return Response(data=None, status=status.HTTP_201_CREATED)
        except:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)