from rest_framework import routers

from tests import mocks


router = routers.DefaultRouter()

router.register(r'stuff',
                mocks.StuffViewSet,
                base_name='stuff')

router.register(r'stuff-linked',
                mocks.StuffHyperlinkedViewSet,
                base_name='stuff-linked')

router.register(r'related-stuff',
                mocks.RelatedStuffViewSet,
                base_name='relatedstuff')

router.register(r'related-stuff-linked',
                mocks.RelatedStuffHyperlinkedViewSet,
                base_name='relatedstuff-linked')

router.register(r'many-related-stuff',
                mocks.RelatedStuffViewSet,
                base_name='manyrelatedstuff')

router.register(r'many-related-stuff-linked',
                mocks.RelatedStuffHyperlinkedViewSet,
                base_name='manyrelatedstuff-linked')

urlpatterns = router.urls
