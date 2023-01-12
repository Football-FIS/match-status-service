from django.shortcuts import render

from .models import MatchStatus
from .serializers import MatchStatusSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import requests, os, json, tweepy


MATCH_SERV_URL = "MATCH_SERV_URL"

#CONEXIONES TWITTER
API_TOKEN = "6helRGOg9XHcjrC6dh2HhmHoZ"
API_TOKEN_SECRET = "U2NuFxLjTnsvNpKAqoQ7lkcfxgnF5ahjrP3nfSdYpcp4ABWjaq"
CONSUMER_KEY = "214587226-t4Ti19gvKp26QqYKzsNRaoqvvAObJaJSHxX8cqLP"
CONSUMER_KEY_SECRET = "M90PxJXLX5AJZon3HRzfTPjuF3lwRSDeN6niLlgoK3z1y"


#No tenemos que crear validate token, debido a que si llega a nuestra api, es porque debes estar logueado (match-service nos controla el acceso por team-service)
match_backend_url = os.getenv(MATCH_SERV_URL, 'https://match-service-danaremar.cloud.okteto.net/') + 'api/v1/'

def send_tweet(minuto, equipos, marcador, info):

    auth = tweepy.OAuthHandler(API_TOKEN, API_TOKEN_SECRET)
    auth.set_access_token(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    api = tweepy.API(auth)
    # Publica un tweet. Suponemos minuto, equipos, marcador, e info provenientes del tipo matchStatus
    api.update_status(str(minuto) + "' | " + str(equipos[0]) + ' ' + str(marcador) + ' ' + str(equipos[1]) + '\n' + str(info))


def match_list(headers):
    # Cambiar headers['Authorization'] por el Bearer xxxxx para probar
    return requests.get(match_backend_url + 'match/list', headers={'Authorization': headers['Authorization']})

def get_match_from_request(request):
    return json.loads(request.content)


class MatchStatusViewSet(viewsets.ModelViewSet):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer


    def list(self, request):

        # extract match list
        bt = match_list(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get match list info
        match = get_match_from_request(bt)

        try:
            # list all matchesStatus with user id coincidence
            queryset = MatchStatus.objects.filter(user_id=match['user_id'])
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

        serializer_class = MatchStatusSerializer(queryset, many=True)
        return Response(serializer_class.data)
