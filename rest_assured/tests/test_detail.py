from . import settings
from .import urls, mocks
from rest_assured.testcases import DetailAPITestCaseMixin


class TestDetailTestCase:

    def get_case(self, **kwargs):
        class MockDetailTestCase(DetailAPITestCaseMixin, mocks.MockTestCase):

            base_name = 'stuff'
            factory_class = mocks.StuffFactory

        self.case_class = MockDetailTestCase

        return MockDetailTestCase(**kwargs)

    def test_get_detail_url(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        assert instance.get_detail_url() == '/stuff/%s/' % instance.object.pk

    def test_get_detail_response(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        assert instance.get_detail_response()

    def test_test_detail(self):
        instance = self.get_case(methodName='dummy')
        instance.setUp()
        response = instance.test_detail()
        assert response
