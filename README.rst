django-rest-assured
===================

.. image:: https://secure.travis-ci.org/ydaniv/django-rest-assured.png
        :target: http://travis-ci.org/ydaniv/django-rest-assured/
        :alt: Build

.. image:: https://pypip.in/download/django-rest-assured/badge.svg
        :target: https://pypi.python.org/pypi/django-rest-assured/
        :alt: Downloads

.. image:: https://pypip.in/version/django-rest-assured/badge.svg
        :target: https://pypi.python.org/pypi/django-rest-assured/
        :alt: Latest Version

.. image:: https://pypip.in/license/django-rest-assured/badge.svg
        :target: https://pypi.python.org/pypi/django-rest-assured/
        :alt: License


Instantly test-cover your Django REST Framework based API.

Django-REST-Assured adds another layer on top of
Django REST Framework's `APITestCase <http://www.django-rest-framework.org/api-guide/testing#test-cases>`_
which allows covering a set of RESTful resource's endpoints with a single class declaration.

This gives both a quick coverage of sanity tests to your API and a more DRY and more friendly
platform for writing additional, more comprehensive tests.


As easy as
----------
.. code-block:: python

    class CategoryTestCase(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):

        base_name = 'category'
        factory_class = CategoryFactory
        create_data = {'name': 'comedy'}
        update_data = {'name': 'horror'}

Django-REST-Assured is designed to work with `factory_boy <http://factoryboy.readthedocs.org/en/latest/>`_
for mocking objects to test against. However, you can easily extend the ``BaseRESTAPITestCase``
to work directly with Django Models or any other factory.


Main features
-------------

* Class-based declarative API for creating tests.
* Covers the stack through: ``route > view > serializer > model``.
* Uses Django REST Framework's conventions to minimize configuration.
* All tests return the response object for more extensive assertions.
* Automatic mocking of authentication if a user factory is provided.


Usage
-----

The basic form of usage is simply to create a class that extends
any mixin from ``rest_assured.testcases``, according to the
endpoints you wish to cover, and the ``BaseRESTAPITestCase`` class.

Then just set the required attributes, and continue extending it from there.

.. admonition:: example

    .. code:: python

        class CategoryAPITestCase(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):

            base_name = 'category'
            factory_class = Category
            create_data = {'name', 'documentary'}
            update_data = {'name', 'horror'}

If your API requires authentication and/or authorization just add
a user factory class. Assuming you use `factory_boy <http://factoryboy.readthedocs.org/en/latest/>`_:

.. admonition:: example

    .. code:: python

        # in some factories.py module in your accounts app
        class User(factory.DjangoModelFactory):

            class Meta:
                model = User
                exclude = ('raw_password',)

            first_name = 'Robert'
            last_name = factory.Sequence(lambda n: 'Paulson the {0}'.format(n))
            email = factory.sequence(lambda n: 'account{0}@example.com'.format(n))
            username = 'mayhem'
            raw_password = '123'
            password = factory.PostGenerationMethodCall('set_password', raw_password)
            is_active = True


        # now back in your tests.py module
        class CategoryAPITestCase(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):

            base_name = 'category'
            factory_class = Category
            # see here:
            user_factory = User
            create_data = {'name', 'documentary'}
            update_data = {'name', 'horror'}



Supports
--------

Tests run against:

* Django 1.6, 1.7, 1.8 & 1.9.
* Django REST Framework 2.4.3, 2.4.4, 3.0, 3.1, 3.2 & 3.3.
* Python 2.7, 3.3, 3.4 & 3.5 (3.2 should work but is not tested).


Installation
------------

PyPI: https://pypi.python.org/pypi/django-rest-assured

.. code-block:: sh

    $ pip install django-rest-assured

Source: https://github.com/ydaniv/django-rest-assured

.. code-block:: sh

    $ git clone https://github.com/ydaniv/django-rest-assured
    $ python setup.py install


Contributing
------------

Issues are tracked in the `github repository <https://github.com/ydaniv/django-rest-assured/issues/>`_.

Pull requests are welcome!


Running tests
-------------

.. code-block:: sh

   $ pip install pytest pytest-django
   $ py.test


License
-------

Django-REST-Assured is distributed under the BSD license.
