from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
    )
from .serializers import MatchStatusSerializer
from .models import MatchStatus
# Create your views here.


class MatchListApiView(ListAPIView):

    serializer_class = MatchStatusSerializer

    def get_queryset(self):
        return MatchStatus.objects.all()

class MatchCreateApiView(CreateAPIView):
    serializer_class = MatchStatusSerializer

class MacthRetrieveApiView(RetrieveAPIView):
    serializer_class = MatchStatusSerializer
    queryset = MatchStatus.objects.filter()

class MatchDestroyApiView(DestroyAPIView):
    serializer_class = MatchStatusSerializer
    queryset = MatchStatus.objects.all()

class MatchUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = MatchStatusSerializer
    queryset = MatchStatus.objects.all()