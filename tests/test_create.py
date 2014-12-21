from rest_assured.testcases import CreateAPITestCaseMixin
from tests import mocks
from tests.models import Stuff


class TestCreateTestCase:
    def get_case(self, **kwargs):
        class MockCreateTestCase(CreateAPITestCaseMixin, mocks.MockTestCase):
            base_name = 'stuff'
            factory_class = mocks.StuffFactory
            create_data = {"name": "moar stuff"}

        self.case_class = MockCreateTestCase

        return MockCreateTestCase(**kwargs)

    def test_get_create_url(self):
        instance = self.get_case(methodName='dummy')
        assert instance.get_create_url() == '/stuff/'

    def test_get_create_data(self):
        instance = self.get_case(methodName='dummy')
        assert instance.get_create_data() is self.case_class.create_data

    def test_get_create_response(self):
        instance = self.get_case(methodName='dummy')
        assert instance.get_create_response()

    def test_test_create(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        response, created = instance.test_create()
        assert response
        assert created
        assert isinstance(created, Stuff)
        assert response.data['name'] == created.name
