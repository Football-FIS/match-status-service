from django.shortcuts import render

from .models import MatchStatus
from .serializers import MatchStatusSerializer
from rest_framework import viewsets

class MatchStatusViewSet(viewsets.ModelViewSet):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer
