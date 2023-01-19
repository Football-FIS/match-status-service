from django.test import TestCase
from django.shortcuts import render, get_object_or_404
from mock import patch

import pytest
from requests import Response

from .views import MatchStatusViewSet
from .models import MatchStatus
from .serializers import MatchStatusSerializer
# Create your tests here.


# """
#     Check create method in MatchStatus.
# """
# @pytest.mark.django_db
# def test_create_match_status(client):
    
#     json_match_status = {
#         "status_type": "GOA",
#         "matchId": "kjfdslkjflsdjsfjl",
#         "info": "Buen golito del bicho",
#         "date": "2023-01-14T18:19:07.031Z",
#         "scoreboard": "5-0"
#         }

#     headers = {
#         'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDQzNDM3LCJpYXQiOjE2NzM5MDc0MzcsImp0aSI6IjMxZjNiMTE3YjczYzQ2NDZhYzFjMWY4NDA1MTFiNTFlIiwidXNlcl9pZCI6MTl9.LcgBuqC3ge3fQ9ih3OqsBDO_VZ6Y5QXxEkUmebp_2ns',
#         'Content-Type': 'application/json'
#         }
    
#     request_url = '/api/v1/match_status/'

#     response = client.post(request_url, data=json_match_status, headers=headers)

#     expected_response = json_match_status
#     print(response)
#     response_dic = dict(response.data)

#     assert response.status_code == 201
#     assert response_dic == expected_response



@pytest.mark.django_db
def test_gest_matchid(client):
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


# @pytest.mark.django_db
# def test_delete_match_status(client):
#     """
#     Check delete method in team.
#     """

#     request_url = '/api/v1/match_status/'

#     res = 'ageBJh0HKnR9oBDW6V4mpKPE'

#     url = request_url + res

#     response = client.delete(url, content_type='application/json', headers={'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDQzNDM3LCJpYXQiOjE2NzM5MDc0MzcsImp0aSI6IjMxZjNiMTE3YjczYzQ2NDZhYzFjMWY4NDA1MTFiNTFlIiwidXNlcl9pZCI6MTl9.LcgBuqC3ge3fQ9ih3OqsBDO_VZ6Y5QXxEkUmebp_2ns'})

#     match_status_count = MatchStatus.objects.filter(id=res).count()

#     assert response.status_code == 204
#     assert match_status_count == 0
