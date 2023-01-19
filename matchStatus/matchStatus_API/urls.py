from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import MatchStatusViewSet, SendTweet


schema_view = get_schema_view(
   openapi.Info(
      title="MATCH STATUS API",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="diegomonsalvesvazquez@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'match-status', MatchStatusViewSet, basename='MatchStatus')

urlpatterns = [
   # path('', include(router.urls)),
   path('match_status/', MatchStatusViewSet.as_view({'post':'create'})),
   path('match_status/<pk>', MatchStatusViewSet.as_view({'get':'get', 'delete':'delete'})),
   path('match_status/matchid/<pk>', MatchStatusViewSet.as_view({'get':'getMatchID'})),
   path('send_tweet', SendTweet.as_view({'post':'post'})),
   #  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   #  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
