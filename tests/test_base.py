from tests import mocks


class TestBaseTestCase:
    def test_get_factory_class(self):
        instance = mocks.MockTestCase(methodName='dummy')
        assert instance.get_factory_class() is mocks.MockFactory

    def test_get_object(self):
        instance = mocks.MockTestCase(methodName='dummy')
        assert isinstance(instance.get_object(instance.get_factory_class()), mocks.MockObject)

    def test_user_exists_and_forced_auth(self):
        instance = mocks.MockTestCase(methodName='dummy')
        instance.setUp()
        assert isinstance(instance.user, mocks.MockUser)
        assert instance.client.handler._force_user is instance.user
