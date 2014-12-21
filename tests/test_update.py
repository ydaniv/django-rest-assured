from rest_assured.testcases import UpdateAPITestCaseMixin
from tests import mocks
from tests.models import Stuff


class TestUpdateTestCase:
    def get_case(self, **kwargs):
        class MockUpdateTestCase(UpdateAPITestCaseMixin, mocks.MockTestCase):
            base_name = 'stuff'
            factory_class = mocks.StuffFactory
            update_data = {"name": "other things"}

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
