from rest_framework import viewsets, serializers

from rest_assured.testcases import BaseRESTAPITestCase
from tests.models import Stuff


class MockObject(object):
    pass


class MockFactory(object):
    @classmethod
    def create(cls):
        return MockObject()


class StuffFactory(object):
    @classmethod
    def create(cls):
        return Stuff.objects.create(name='name of stuff')


class MockUser(object):
    def get_username(self):
        return 'username'

    def is_authenticated(self):
        return True

    def has_perms(self, perms):
        return True


class MockUserFactory(object):
    @classmethod
    def create(cls):
        return MockUser()


class MockTestCase(BaseRESTAPITestCase):
    factory_class = MockFactory
    user_factory = MockUserFactory

    def __init__(self, *args, **kwargs):
        self._pre_setup()
        super(MockTestCase, self).__init__(*args, **kwargs)

    def _pre_setup(self):
        self.client = self.client_class()

    def dummy(self):
        pass


class StuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff


class StuffViewSet(viewsets.ModelViewSet):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    paginate_by = 10
