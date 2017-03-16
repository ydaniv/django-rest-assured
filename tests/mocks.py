from rest_framework import viewsets, serializers

from rest_assured.testcases import BaseRESTAPITestCase
from tests.models import Stuff, RelatedStuff, ManyRelatedStuff


class MockObject(object):
    pass


class MockFactory(object):
    @classmethod
    def create(cls):
        return MockObject()


class StuffFactory(object):
    @classmethod
    def create(cls, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'name of stuff'
        if 'answer' not in kwargs:
            kwargs['answer'] = 42
        return Stuff.objects.create(**kwargs)


class RelatedStuffFactory(object):
    @classmethod
    def create(cls):
        thing = Stuff.objects.create(name='referenced stuff')
        return RelatedStuff.objects.create(thing=thing)


class ManyRelatedStuffFactory(object):
    @classmethod
    def create(cls):
        thing1 = Stuff.objects.create(name='referenced stuff 1')
        thing2 = Stuff.objects.create(name='referenced stuff 2')
        obj = ManyRelatedStuff.objects.create()
        obj.stuff.add(thing1, thing2)
        return obj


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


class StuffHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stuff


class RelatedStuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedStuff


class RelatedStuffHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelatedStuff

    thing = serializers.HyperlinkedRelatedField(queryset=Stuff.objects.all(),
                                                view_name='stuff-linked-detail')


class ManyRelatedStuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManyRelatedStuff


class ManyRelatedStuffHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManyRelatedStuff

    # stuff = serializers.HyperlinkedRelatedField(queryset=Stuff.objects.all(),
    #                                             many=True)


class StuffViewSet(viewsets.ModelViewSet):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    paginate_by = 10


class StuffHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = Stuff.objects.all()
    serializer_class = StuffHyperlinkedSerializer
    paginate_by = 10


class RelatedStuffViewSet(viewsets.ModelViewSet):
    queryset = RelatedStuff.objects.all()
    serializer_class = RelatedStuffSerializer
    paginate_by = 10


class RelatedStuffHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = RelatedStuff.objects.all()
    serializer_class = RelatedStuffHyperlinkedSerializer
    paginate_by = 10


class ManyRelatedStuffViewSet(viewsets.ModelViewSet):
    queryset = ManyRelatedStuff.objects.all()
    serializer_class = ManyRelatedStuffSerializer
    paginate_by = 10


class ManyRelatedStuffHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = ManyRelatedStuff.objects.all()
    serializer_class = ManyRelatedStuffHyperlinkedSerializer
    paginate_by = 10
