from rest_framework import routers

from tests import mocks


router = routers.DefaultRouter()

router.register(r'stuff', mocks.StuffViewSet, base_name='stuff')

urlpatterns = router.urls
