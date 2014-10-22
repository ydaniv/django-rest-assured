from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BaseRESTAPITestCase(APITestCase):

    """Base test case class for testing REST API endpoints."""

    LIST_SUFFIX = '-list'
    DETAIL_SUFFIX = '-detail'
    lookup_field = 'pk'
    factory_class = None
    use_token_auth = False

    def get_factory_class(self):
        """Return the factory class for generating the main object (or model instance) of this test case.

        By default this gets the ``factory_class`` attribute of this class.

        :returns Factory class used for creating the mock objects."""

        return getattr(self, 'factory_class')

    def get_object(self, factory):
        """Create and return the object (or model instance) of this test case.

        By default this calls the ``create()`` method of the factory class, assuming
        a Django Model or a factory_boy's Factory.

        :param factory: The factory class used for creating
        :returns The main object of this test case."""

        return factory.create()

    def get_credentials(self, user):
        """Return the credentials dictionary.

        By default this consists getting the ``username`` field of the ``user`` instance
        and the ``raw_password`` attribute of the ``user_factory`` attribute of this class.

        :param user: The user instance that will be used to login.
        :returns A dictionary of credentials for user login."""

        return {
            'username': user.get_username(),
            'password': self.user_factory.raw_password}

    def setUp(self):
        """Generates the main object and user instance if needed.

        The user will also be logged in automatically, using the ``login()`` method of the test's client.
        You can opt for token authentication by setting the class' ``use_token_auth`` to ``True``.

        The user instance will be created only if the ``user_factory`` attribute is set to the factory class."""

        # create the object
        self.object = self.get_object(self.get_factory_class())

        # create a user and log in to get permissions
        user_factory = getattr(self, 'user_factory', None)
        if user_factory:
            self.user = user_factory.create()
            if self.use_token_auth:
                token = Token.objects.get(user=self.user)
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            else:
                self.client.login(**self.get_credentials(self.user))


class ListAPITestCaseMixin(object):

    """Adds the ``listview()`` method for testing list API endpoints."""

    def listview(self, **kwargs):
        """Send request to the list view endpoint, verify and return the response.

        Checks for a 200 status code and that there is a ``results`` property in the ``response.data``.

        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns The view's response."""

        listview = reverse(self.base_name + self.LIST_SUFFIX)
        response = self.client.get(listview, **kwargs)

        if response.status_code != status.HTTP_200_OK:
            print '\n%s' % response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        return response


class DetailAPITestCaseMixin(object):

    """Adds the ``detailview()`` method for testing detail API endpoints."""

    def detailview(self, **kwargs):
        """Send request to the detail view endpoint, verify and return the response.

        Checks for a 200 status code and that there is an ``id`` property in the ``response.data``
        and that it equals the main object's id.

        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns The view's response."""

        object_id = getattr(self.object, self.lookup_field)

        detailview = reverse(self.base_name + self.DETAIL_SUFFIX, args=[unicode(object_id)])
        response = self.client.get(detailview, **kwargs)

        if response.status_code != status.HTTP_200_OK:
            print '\n%s' % response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode(self.object.id), response.data['id'])

        return response


class CreateAPITestCaseMixin(object):

    """Adds the ``createview()`` method for testing create API endpoints."""

    def createview(self, data=None, **kwargs):
        """Send request to the create view endpoint, verify and return the response.

        Also verifies that the object actually exists in the database.

        :param data: A dictionary of the data to use for the create request.
        :param kwargs: Extra arguments that are passed to the client's ``post()`` call.
        :returns The view's response."""

        create_view = reverse(self._get_create_name())
        response = self.client.post(create_view, data or {}, **kwargs)

        if response.status_code != status.HTTP_201_CREATED:
            print '\n%s' % response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # getting the instance from database simply to see that it's found and does not raise any exception
        self.object.__class__.objects.get(id=response.data.get('id'))

        return response

    def _get_create_name(self):
        if hasattr(self, 'create_name'):
            view_name = self.create_name
        else:
            view_name = self.base_name + self.LIST_SUFFIX

        return view_name


class DestroyAPITestCaseMixin(object):

    """Adds the ``destroyview()`` method for testing destroy API endpoints."""

    def destroyview(self, **kwargs):
        """Send request to the destroy view endpoint, verify and return the response.

        Also verifies the object does not exist anymore in the database.

        :param kwargs: Extra arguments that are passed to the client's ``delete()`` call.
        :returns The view's response."""

        object_id = getattr(self.object, self.lookup_field)

        destroyview = reverse(self._get_destroy_name(),
                              args=(object_id,))
        response = self.client.delete(destroyview, **kwargs)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(ObjectDoesNotExist, self.object.__class__.objects.get, **{self.lookup_field: object_id})

        return response

    def _get_destroy_name(self):
        if hasattr(self, 'destroy_name'):
            view_name = self.destroy_name
        else:
            view_name = self.base_name + self.DETAIL_SUFFIX

        return view_name


class UpdateAPITestCaseMixin(object):

    """Adds the ``updateview()`` method for testing update API endpoints."""

    def updateview(self, data=None, results=None, patch=True, **kwargs):
        """Send request to the update view endpoint, verify and return the response.

        :param data: Data dictionary for the update request.
        :param results: Dictionary mapping instance properties to expected values.
        :param kwargs: Extra arguments that are passed to the client's ``put()`` or ``patch()`` call.
        :returns The view's response."""

        object_id = getattr(self.object, self.lookup_field)
        updateview = reverse(self._get_update_name(),
                             args=(object_id,))
        args = [updateview, data]
        response = self.client.patch(*args, **kwargs) if patch else self.client.put(*args, **kwargs)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print '\n%s' % response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # getting a fresh copy of the object from DB
        obj = self.object.__class__.objects.get(**{self.lookup_field: object_id})
        self._update_check_db(obj, data, results)

        return response

    def _get_update_name(self):
        if hasattr(self, 'update_name'):
            view_name = self.update_name
        else:
            view_name = self.base_name + self.DETAIL_SUFFIX

        return view_name

    def _update_check_db(self, obj, data, results):
        if results is None:
            results = {}

        for key, value in data.iteritems():
            # check for foreign key
            if hasattr(obj, '%s_id' % key):
                related = getattr(obj, key)
                # hack to check if there's a uuid field and use it instead of pk
                # because of the issue with setting it as primary for Accounts
                if hasattr(related, 'uuid'):
                    attribute = unicode(related.uuid)
                else:
                    attribute = unicode(related.pk)
            else:
                attribute = getattr(obj, key)
                # Handle case of a ManyToMany relation
                if isinstance(attribute, Manager):
                    for pk in value:
                        self.assertIn(pk, [unicode(item.pk) for item in attribute.all()])
                    return True

            self.assertEqual(attribute, results.get(key, value))


class ReadAPITestCaseMixin(ListAPITestCaseMixin, DetailAPITestCaseMixin):

    """Adds the read CRUD operations tests to the test case."""

    pass


class WriteAPITestCaseMixin(CreateAPITestCaseMixin, UpdateAPITestCaseMixin, DestroyAPITestCaseMixin):

    """Adds the write CRUD operations tests to the test case."""

    pass


class RESTAPITestCase(ReadAPITestCaseMixin, WriteAPITestCaseMixin, BaseRESTAPITestCase):

    """A complete API test case that covers all successful CRUD operation requests."""

    pass
