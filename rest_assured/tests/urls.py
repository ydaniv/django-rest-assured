from django.conf.urls import patterns, url, include
from rest_framework import routers
from . import mocks


router = routers.DefaultRouter()

router.register(r'stuff', mocks.StuffViewSet, base_name='stuff')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
