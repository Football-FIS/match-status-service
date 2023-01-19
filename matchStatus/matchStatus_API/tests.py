from django.db import connections
from django.db.utils import OperationalError
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework.response import Response
from .models import MatchStatus, Tweet
from .views import MatchStatusViewSet, SendTweet
from .serializers import MatchStatusSerializer
import os
import requests
import pytest
# Create your tests here.


def mock_create(datos):
    serializador = MatchStatusSerializer(data=datos)
    if serializador.is_valid():
        serializador.save()
        return Response(serializador.data, status=201)
    else:
        return Response(serializador.data, status=400)




class Testing(TestCase):

    """
    INTEGRATION MONGODB TEST: 
    Check if connects to DB
    """
    @pytest.mark.django_db
    def test_mongo_db_conn(self):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            assert False
        else:
            assert True

    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in MatchStatus.
    """
    @pytest.mark.django_db
    def test_create_match_status(client):
        
        json_match_status = {
            "status_type": "GOA",
            "matchId": "kjfdslkjflsdjsfjl",
            "info": "Buen golito del bicho",
            "date": "2023-01-14T18:19:07.031Z",
            "scoreboard": "5-0"
            }

        request_url = '/api/v1/match_status/'

        MatchStatusViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchStatusViewSet.create(json_match_status)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 201

    
    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in MatchStatus without matchId.
    """
    @pytest.mark.django_db
    def test_bad_create_match_status(client):
        
        json_match_status = {
            "status_type": "GOA",
            "info": "Buen golito del bicho",
            "date": "2023-01-14T18:19:07.031Z",
            "scoreboard": "5-0"
            }

        request_url = '/api/v1/match_status/'

        MatchStatusViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchStatusViewSet.create(json_match_status)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 400


    """
        COMPONENT / DB INTEGRATION TEST:
        Check delete method in matchStatus.
    """
    @pytest.mark.django_db
    def test_delete_match(self):

        def mock_delete(id):
            
            match = MatchStatus.objects.filter(id=id)
            if(match):
                match.delete()
                return Response(status=204)
            else:
                return Response(status=404)
        

        objeto = MatchStatus.objects.create(
            status_type = "STA",
            matchId = "15622",
            info = "Comienza el encuentro en Pilas",
            date = "2023-01-12T22:39:36.695000Z",
            scoreboard = "0-0"
        )
        
        MatchStatusViewSet.delete = mock_delete
        
        response = MatchStatusViewSet.delete(objeto.id)
        match_count = MatchStatus.objects.filter(id=objeto.id).count()

        assert response.status_code == 204
        assert match_count == 0


    """
        COMPONENT / DB INTEGRATION TEST:
        Check bad delete method in matchStatus.
    """
    @pytest.mark.django_db
    def test_bad_delete_match(self):

        def mock_delete(id):
            
            match = MatchStatus.objects.filter(id=id)
            if(match):
                match.delete()
                return Response(status=204)
            else:
                return Response(status=404)
        

        objeto = MatchStatus.objects.create(
            status_type = "STA",
            matchId = "15622",
            info = "Comienza el encuentro en Pilas",
            date = "2023-01-12T22:39:36.695000Z",
            scoreboard = "0-0"
        )
        
        MatchStatusViewSet.delete = mock_delete
        objeto.id = "adsfjdasjd"

        response = MatchStatusViewSet.delete(objeto.id)
        match_count = MatchStatus.objects.filter(id=objeto.id).count()

        assert response.status_code == 404
        assert match_count == 0

    """
        INTEGRATION TEST: 
        Check send tweet correctly
    """
    @pytest.mark.django_db
    def test_send_tweet(client):
        
        json_match_status = {
            "status_type": "GOA",
            "matchId": "kjfdslkjflsdjsfjl",
            "info": "Buen golito del bicho",
            "date": "2023-01-14T18:19:07.031Z",
            "scoreboard": "5-0"
            }

        request_url = '/api/v1/match_status/'

        SendTweet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = SendTweet.create(json_match_status)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 201
    
    """
        INTEGRATION TEST: 
        Check send tweet bad by more than 240 charact
    """
    @pytest.mark.django_db
    def test_bad_send_tweet(client):
        
        json_match_status = {
            "status_type": "GOA",
            "matchId": "kjfdslkjflsdjsfjljjkldasfdjkashlkjahfkjlahdfkjlhafskjlhfdalkjshkjlfashjkhaskjlhfakljhdflahsdfjhfdsahfdsahaklhfdklashdfjklahdjfklhafskjlhfakjslhfkjlashfdklahfdkjlahsfkjlhafkjlhafdkjlhfadskjlhdfjklahfdkljhafklhaflkjhfakjlhfklahskjlfadskljhfdkjalhdfkljablfahslfhasldkfhalfdhlakdjhfkjladsfj",
            "info": "Buen golito del bicho",
            "date": "2023-01-14T18:19:07.031Z",
            "scoreboard": "5-0"
            }

        request_url = '/api/v1/match_status/'

        SendTweet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = SendTweet.create(json_match_status)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 400


"""
    INTEGRATION TEST: 
    Check get by matchId
"""
@pytest.mark.django_db
def test_get_matchid(client):
    """
    Check get match id method in match status.
    """

    request_url = '/api/v1/match_status/matchid/'

    pk = 'kjfdslkjflsdjsfjl'
    
    response = client.get(request_url+pk)

    expected = [
                    {
                        "id": "xpcKciX0MuOSLnNeFu0gJwgE",
                        "status_type": "STA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "Comienza el encuentro",
                        "date": "2023-01-18T17:49:28.074000Z",
                        "scoreboard": "0-0"
                    },
                    {
                        "id": "xpcKciX0MuOSLnNeFu0gJwgE",
                        "status_type": "GOA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "GOOOOOOOOOL DE MARCISO",
                        "date": "2023-01-18T17:49:50.201000Z",
                        "scoreboard": "1-0"
                    },
                    {
                        "id": "xpcKciX0MuOSLnNeFu0gJwgE",
                        "status_type": "GOA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "GOOOOOOOOOOOOOOOOOL EN PP",
                        "date": "2023-01-18T17:50:12.961000Z",
                        "scoreboard": "55-2"
                    },
                    {
                        "id": "xpcKciX0MuOSLnNeFu0gJwgE",
                        "status_type": "GOA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "Gulaso de Bruno",
                        "date": "2023-01-18T17:52:28.844000Z",
                        "scoreboard": "649-3615"
                    },
                    {
                        "id": "xpcKciX0MuOSLnNeFu0gJwgE",
                        "status_type": "GOA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "ajsdfhkljdsf",
                        "date": "2023-01-18T18:00:53.627000Z",
                        "scoreboard": "55-4"
                    },
                    {
                        "id": "YX7JMCkRpwgY3OL9I3bQSL2U",
                        "status_type": "GOA",
                        "matchId": "kjfdslkjflsdjsfjl",
                        "info": "Gulaso de Loren Gorrión",
                        "date": "2023-01-19T00:08:02.797000Z",
                        "scoreboard": "5-0"
                    }
                ]

    matchStatus = MatchStatus.objects.all()
    expected_data = MatchStatusSerializer(expected, many=True).data

    assert response.status_code == 200

