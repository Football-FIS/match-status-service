from django.urls import path, include
from rest_framework import routers

from .views import MatchStatusViewSet


router = routers.DefaultRouter()
router.register(r'match-status', MatchStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
