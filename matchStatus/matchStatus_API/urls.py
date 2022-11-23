from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('matchStatus/', views.MatchCreateApiView.as_view()),
    path('matchStatus/<pk>', views.MacthRetrieveApiView.as_view()),
]