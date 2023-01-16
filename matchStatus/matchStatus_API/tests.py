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
# @patch('matchStatus_API.views.validate_token')
# def test_create_match_status(validate_token, client):
    
#     validate_token.status_code.return_value = 200

#     json_match_status = {
#                 "status_type": "GOA",
#                 "matchId": "ajfdnajfhdid",
#                 "user_id": 2147483647,
#                 "info": "Golazo de Perico",
#                 "date": "2023-01-14T18:19:07.031Z",
#                 "scoreboard": "0-1",
#                 "uidPlayer": "Periko12"
#             }
    
#     request_url = '/api/v1/match_status/'

#     response = client.post(request_url, data=json_match_status, format='json', headers={'Authorization' : 'Bearer test'})

#     expected_response = json_match_status
#     response_dic = dict(response.data)

#     assert response.status_code == 201
#     assert response_dic == expected_response



# @pytest.mark.django_db
# def test_gest_matchid(client):
#     """
#     Check get match id method in match status.
#     """

#     request_url = '/api/v1/match_status/matchid/'

#     pk = 'string'
    
#     response = client.get(request_url+pk)

#     matchStatus = MatchStatus.objects.all()
#     expected_data = MatchStatusSerializer(matchStatus, many=True).data

#     assert response.status_code == 200


@pytest.mark.django_db
def test_delete_match_status(client):
    """
    Check delete method in team.
    """

    request_url = '/api/v1/match_status/'

    res = 'ageBJh0HKnR9oBDW6V4mpKPE'

    url = request_url + res

    response = client.delete(url, content_type='application/json', headers={'Authorization' : 'Bearer test'})

    match_status_count = MatchStatus.objects.filter(id=res).count()

    assert response.status_code == 204
    assert match_status_count == 0
