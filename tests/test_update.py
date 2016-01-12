from django.test import TestCase

from rest_framework.reverse import reverse
from rest_assured.testcases import UpdateAPITestCaseMixin
from tests import mocks
from tests.models import Stuff, RelatedStuff


class TestUpdateTestCase(TestCase):
    def get_case(self, **kwargs):
        class MockUpdateTestCase(UpdateAPITestCaseMixin, mocks.MockTestCase):
            base_name = kwargs.pop('base_name', 'stuff')
            factory_class = mocks.StuffFactory
            update_data = {'name': 'other things'}

        self.case_class = MockUpdateTestCase

        return MockUpdateTestCase(**kwargs)

    def get_related_case(self, **kwargs):
        class MockUpdateTestCase(UpdateAPITestCaseMixin, mocks.MockTestCase):
            base_name = 'relatedstuff'
            factory_class = mocks.RelatedStuffFactory
            other_thing = mocks.StuffFactory.create(name='other related thing')
            update_data = {'thing': other_thing.id}
            update_results = {'thing': str(other_thing.id)}

        self.case_class = MockUpdateTestCase

        return MockUpdateTestCase(**kwargs)

    def get_related_linked_case(self, **kwargs):
        class MockUpdateTestCase(UpdateAPITestCaseMixin, mocks.MockTestCase):
            base_name = 'relatedstuff-linked'
            factory_class = mocks.RelatedStuffFactory
            other_thing = mocks.StuffFactory.create(name='other related thing')
            related_url = reverse('stuff-linked-detail', (other_thing.id,))
            update_data = {'thing': related_url}
            update_results = {'thing': related_url}

            def get_relationship_value(self, related, key):
                return reverse('stuff-linked-detail', (related.id,))

        self.case_class = MockUpdateTestCase

        return MockUpdateTestCase(**kwargs)

    def get_many_related_case(self, **kwargs):
        class MockUpdateTestCase(UpdateAPITestCaseMixin, mocks.MockTestCase):
            base_name = kwargs.pop('base_name', 'manyrelatedstuff')
            factory_class = mocks.ManyRelatedStuffFactory

            def get_update_data(self):
                other_thing = mocks.StuffFactory.create(name='other related thing')
                another_thing = mocks.StuffFactory.create(name='another related thing')
                return {'stuff': [other_thing.id, another_thing.id]}

        self.case_class = MockUpdateTestCase

        return MockUpdateTestCase(**kwargs)

    def test_get_update_url(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        assert instance.get_update_url() == '/stuff/%s/' % instance.object.pk

    def test_get_update_data(self):
        instance = self.get_case(methodName='dummy')
        assert instance.get_update_data() is self.case_class.update_data

    def test_get_update_response(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        assert instance.get_update_response()

    def test_test_update(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        response, updated = instance.test_update()
        assert response
        assert updated
        assert isinstance(updated, Stuff)
        assert response.data['name'] == updated.name

    def test_test_update_with_foreignkey(self):
        instance = self.get_related_case(methodName='dummy')
        instance.setUp()
        response, updated = instance.test_update()
        assert response
        assert updated
        assert isinstance(updated, RelatedStuff)
        assert response.data['thing'] == updated.thing.id

    def test_test_update_with_foreignkey_and_hyperlinkedmodelserializer(self):
        instance = self.get_related_linked_case(methodName='dummy')
        instance.setUp()
        response, updated = instance.test_update()
        assert response
        assert updated
        assert isinstance(updated, RelatedStuff)
