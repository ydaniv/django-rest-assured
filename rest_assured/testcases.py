from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.utils.six import text_type


class BaseRESTAPITestCase(APITestCase):

    """Base test case class for testing REST API endpoints."""

    #: *required*: Base route name of the API endpoints to test.
    base_name = None
    #: *required*: The factory class to use for creating the main object to test against.
    factory_class = None
    #: Suffix for list endpoint view names. Defaults to ``'-list'``.
    LIST_SUFFIX = '-list'
    #: Suffix for detail endpoint view names. Defaults to ``'-detail'``.
    DETAIL_SUFFIX = '-detail'
    #: The field to use for DB and route lookups. Defaults to ``'pk'``.
    lookup_field = 'pk'
    #: User factory to use in case you need user authentication for testing. Defaults to ``None``.
    user_factory = None
    #: The main test subject.
    object = None
    #: The user instance created if the ``user_factory`` is set and used. Defaults to ``None``.
    user = None

    def get_factory_class(self):
        """Return the factory class for generating the main object (or model instance) of this test case.

        By default this gets the ``factory_class`` attribute of this class.

        :returns: Factory class used for creating the mock objects.
        """

        return getattr(self, 'factory_class')

    def get_object(self, factory):
        """Create and return the object (or model instance) of this test case.

        By default this calls the ``create()`` method of the factory class, assuming
        a Django Model or a factory_boy's Factory.

        :param factory: The factory class used for creating
        :returns: The main object of this test case.
        """

        return factory.create()

    def setUp(self):
        """Generates the main object and user instance if needed.

        The user instance will be created only if the ``user_factory`` attribute is set to the factory class.

        If there is an available user instance, that user will be force authenticated.
        """

        # create and force authenticate user
        user_factory = getattr(self, 'user_factory')
        if user_factory:
            self.user = user_factory.create()
            self.client.force_authenticate(self.user)

        # create the object
        self.object = self.get_object(self.get_factory_class())


class ListAPITestCaseMixin(object):

    """Adds a list view test to the test case."""

    #: When using pagination set this attribute to the name of the property in the response data that holds the result set. Defaults to ``None``.
    pagination_results_field = None

    def get_list_url(self):
        """Return the list endpoint url.

        :returns: The url of list endpoint.
        """

        return reverse(self.base_name + self.LIST_SUFFIX)

    def get_list_response(self, **kwargs):
        """Send the list request and return the response.

        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns: The response object.
        """

        return self.client.get(self.get_list_url(), **kwargs)

    def test_list(self, **kwargs):
        """Send request to the list view endpoint, verify and return the response.

        Checks for a 200 status code and that there is a ``results`` property in the ``response.data``.

        You can extend it for more extensive checks.

        .. admonition:: example

            .. code:: python

                class LanguageRESTAPITestCase(ListAPITestCaseMixin, BaseRESTAPITestCase):

                    def test_list(self, **kwargs):
                        response = super(LanguageRESTAPITestCase, self).test_list(**kwargs)
                        results = response.data.get('results')
                        self.assertEqual(results[0].get('code'), self.object.code)

        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns: The view's response.
        """

        response = self.get_list_response(**kwargs)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        results = response.data

        if self.pagination_results_field:
            self.assertIn(self.pagination_results_field, response.data)
            results = results[self.pagination_results_field]

        self.assertTrue(len(results) >= 1)

        return response


class DetailAPITestCaseMixin(object):

    """Adds a detail view test to the test case."""

    # A list of attribute names to check equality between the main object and the response data.
    # Defaults to ``['id']``.
    # You can also use a tuple of a string and a callable, that takes the object and returns an attribute's value.
    attributes_to_check = ['id']

    def get_detail_url(self):
        """Return the detail endpoint url.

        :returns: The url of detail endpoint.
        """

        object_id = getattr(self.object, self.lookup_field)
        return reverse(self.base_name + self.DETAIL_SUFFIX, args=[text_type(object_id)])

    def get_detail_response(self, **kwargs):
        """Send the detail request and return the response.

        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns: The response object.
        """

        return self.client.get(self.get_detail_url(), **kwargs)

    def test_detail(self, **kwargs):
        """Send request to the detail view endpoint, verify and return the response.

        Checks for a 200 status code and that there is an ``id`` property in the ``response.data``
        and that it equals the main object's id.

        You can extend it for more extensive checks.

        .. admonition:: example

            .. code:: python

                class LanguageRESTAPITestCase(DetailAPITestCaseMixin, BaseRESTAPITestCase):

                    def test_list(self, **kwargs):
                        response = super(LanguageRESTAPITestCase, self).test_list(**kwargs)
                        self.assertEqual(response.data.get('code'), self.object.code)

        Using a callable in ``attributes_to_check``:

        .. admonition:: example

            .. code:: python

                class TaggedFoodRESTAPITestCase(DetailAPITestCaseMixin, BaseRESTAPITestCase):

                    attributes_to_check = ['name', ('similar', lambda obj: obj.tags.similar_objects())]


        :param kwargs: Extra arguments that are passed to the client's ``get()`` call.
        :returns: The view's response.
        """

        response = self.get_detail_response(**kwargs)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self._check_attributes(response.data)

        return response

    def _check_attributes(self, data):
        for attr in self.attributes_to_check:
            if isinstance(attr, (tuple, list, set)):
                value = text_type(attr[1](self.object))
                attr = attr[0]
            else:
                value = text_type(getattr(self.object, attr))

            self.assertEqual(value, text_type(data[attr]))


class CreateAPITestCaseMixin(object):

    """Adds a create view test to the test case."""

    #: *required*: Dictionary of data to use as the POST request's body.
    create_data = None
    #: The name of the field in the response data for looking up the created object in DB.
    response_lookup_field = 'id'

    def get_create_data(self):
        """Return the data used for the create request.

        By default gets the ``create_data`` attribute of this class.

        :returns: The data dictionary.
        """

        return getattr(self, 'create_data')

    def get_create_url(self):
        """Return the create endpoint url.

        :returns: The url of create endpoint.
        """

        return reverse(self._get_create_name())

    def get_create_response(self, data=None, **kwargs):
        """Send the create request and return the response.

        :param data: A dictionary of the data to use for the create request.
        :param kwargs: Extra arguments that are passed to the client's ``post()`` call.
        :returns: The response object.
        """

        if data is None:
            data = self.get_create_data()

        return self.client.post(self.get_create_url(), data or {}, **kwargs)

    def get_lookup_from_response(self, data):
        """Return value for looking up the created object in DB.

        :Note: The created object will be looked up using the ``lookup_field`` attribute as key, which defaults to ``pk``.

        :param data: A dictionary of the response data to lookup the field in.
        :returns: The value for looking up the
        """
        return data.get(self.response_lookup_field)

    def test_create(self, data=None, **kwargs):
        """Send request to the create view endpoint, verify and return the response.

        Also verifies that the object actually exists in the database.

        :param data: A dictionary of the data to use for the create request.
        :param kwargs: Extra arguments that are passed to the client's ``post()`` call.
        :returns: A tuple ``response, created`` of the view's response the created instance.
        """

        response = self.get_create_response(data, **kwargs)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, getattr(response, 'data', response))

        # another sanity check:
        # getting the instance from database simply to see that it's found and does not raise any exception
        created = self.object.__class__.objects.get(
            **{self.lookup_field: self.get_lookup_from_response(response.data)})

        return response, created

    def _get_create_name(self):
        if hasattr(self, 'create_name'):
            view_name = self.create_name
        else:
            view_name = self.base_name + self.LIST_SUFFIX

        return view_name


class DestroyAPITestCaseMixin(object):

    """Adds a destroy view test to the test case."""

    def get_destroy_url(self):
        """Return the destroy endpoint url.

        :returns: The url of destroy endpoint.
        """

        self.object_id = getattr(self.object, self.lookup_field)
        return reverse(self._get_destroy_name(),
                       args=(self.object_id,))

    def get_destroy_response(self, **kwargs):
        """Send the destroy request and return the response.

        :param kwargs: Extra arguments that are passed to the client's ``delete()`` call.
        :returns: The view's response.
        """

        return self.client.delete(self.get_destroy_url(), **kwargs)

    def test_destroy(self, **kwargs):
        """Send request to the destroy view endpoint, verify and return the response.

        Also verifies the object does not exist anymore in the database.

        :param kwargs: Extra arguments that are passed to the client's ``delete()`` call.
        :returns: The view's response.
        """

        response = self.get_destroy_response(**kwargs)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        # Another sanity check:
        # see that the instance is removed from the database.
        self.assertRaises(ObjectDoesNotExist, self.object.__class__.objects.get, **{self.lookup_field: self.object_id})

        return response

    def _get_destroy_name(self):
        if hasattr(self, 'destroy_name'):
            view_name = self.destroy_name
        else:
            view_name = self.base_name + self.DETAIL_SUFFIX

        return view_name


class UpdateAPITestCaseMixin(object):

    """Adds an update view test to the test case."""

    #: Whether to send a PATCH request instead of PUT. Defaults to ``True``.
    use_patch = True
    #: *required*: Dictionary of data to use as the update request's body.
    update_data = None
    #: Dictionary mapping attributes to values to check against the updated instance in the database.
    #: Defaults to ``update_data``.
    update_results = None
    #: The name of the field in the response data for looking up the created object in DB.
    relationship_lookup_field = 'id'

    def get_update_url(self):
        """Return the update endpoint url.

        :returns: The url of update endpoint.
        """

        self.object_id = getattr(self.object, self.lookup_field)
        return reverse(self._get_update_name(),
                       args=(self.object_id,))

    def get_update_response(self, data=None, results=None, use_patch=None, **kwargs):
        """Send the update request and return the response.

        :param data: Data dictionary for the update request.
        :param results: Dictionary mapping instance properties to expected values.
        :param kwargs: Extra arguments that are passed to the client's ``put()`` or ``patch()`` call.
        :returns: The response object.
        """

        if data is None:
            data = self.get_update_data()
            self.__data = data

        if results is None:
            results = self.get_update_results(data)
            self.__results = results

        args = [self.get_update_url(), data]

        if use_patch is None:
            use_patch = self.use_patch

        return self.client.patch(*args, **kwargs) if use_patch else self.client.put(*args, **kwargs)

    def get_update_data(self):
        """Return the data used for the update request.

        By default gets the ``update_data`` attribute of this class.

        :returns: Data dictionary for the update request.
        """

        return getattr(self, 'update_data')

    def get_update_results(self, data=None):
        """Return a dictionary of the expected results of the instance.

        By default gets the ``update_results`` attribute of this class.
        If that isn't set defaults to the data.

        :param data: The update request's data dictionary.
        :returns: Dictionary mapping instance properties to expected values.
        """

        return getattr(self, 'update_results', data)

    def get_relationship_value(self, related_obj, key):
        """Return a value representing a relation to a related model instance.

        By default gets the ``relationship_lookup_field`` attribute of this class
        which defaults to ``id``, and converts it to a ``string``.

        :param related_obj: The related model instance to convert to a value.
        :param key: A ``string`` representing the name of the relation, or the key on the updated object.
        :returns: Value representing the relation to assert against.
        """

        return text_type(getattr(related_obj, getattr(self, 'relationship_lookup_field')))

    def test_update(self, data=None, results=None, use_patch=None, **kwargs):
        """Send request to the update view endpoint, verify and return the response.

        :param data: Data dictionary for the update request.
        :param results: Dictionary mapping instance properties to expected values.
        :param kwargs: Extra arguments that are passed to the client's ``put()`` or ``patch()`` call.
        :returns: A tuple ``response, updated`` of the view's response the updated instance.
        """

        response = self.get_update_response(data, results, use_patch, **kwargs)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        # getting a fresh copy of the object from DB
        updated = self.object.__class__.objects.get(**{self.lookup_field: self.object_id})
        # Sanity check:
        # check that the copy in the database was updated as expected.
        self._update_check_db(updated, data, results)

        return response, updated

    def _get_update_name(self):
        if hasattr(self, 'update_name'):
            view_name = self.update_name
        else:
            view_name = self.base_name + self.DETAIL_SUFFIX

        return view_name

    def _update_check_db(self, obj, data=None, results=None):
        if data is None:
            data = self.__data

        if results is None:
            results = self.__results or {}

        for key, value in six.iteritems(data):
            # check if ``obj`` is a dict to allow overriding ``_update_check_db()``
            # and perform checks on a serialized object
            if isinstance(obj, dict):
                attribute = obj.get(key)
                if isinstance(attribute, list):
                    self.assertListEqual(attribute, value)
                    continue
            else:
                # check for foreign key
                if hasattr(obj, '%s_id' % key):
                    related = getattr(obj, key)
                    attribute = self.get_relationship_value(related, key)
                else:
                    attribute = getattr(obj, key)
                    # Handle case of a ManyToMany relation
                    if isinstance(attribute, Manager):
                        items = {self.get_relationship_value(item, key) for item in attribute.all()}
                        self.assertTrue(set(value).issubset(items))
                        continue

            self.assertEqual(attribute, results.get(key, value))


class ReadRESTAPITestCaseMixin(ListAPITestCaseMixin, DetailAPITestCaseMixin):

    """Adds the read CRUD operations tests to the test case.

    Includes: :class:`ListAPITestCaseMixin`, :class:`DetailAPITestCaseMixin`.
    """

    pass


class WriteRESTAPITestCaseMixin(CreateAPITestCaseMixin, UpdateAPITestCaseMixin, DestroyAPITestCaseMixin):

    """Adds the write CRUD operations tests to the test case.

    Includes: :class:`CreateAPITestCaseMixin`, :class:`UpdateAPITestCaseMixin`, :class:`DestroyAPITestCaseMixin`.
    """

    pass


class ReadWriteRESTAPITestCaseMixin(ReadRESTAPITestCaseMixin, WriteRESTAPITestCaseMixin):

    """A complete API test case that covers all successful CRUD operation requests.

    Includes: :class:`ReadRESTAPITestCaseMixin`, :class:`WriteRESTAPITestCaseMixin`.
    """

    pass
