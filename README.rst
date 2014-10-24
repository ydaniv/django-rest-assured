.. django-rest-assured documentation master file, created by
   sphinx-quickstart on Fri Oct 24 10:48:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


django-rest-assured
===================

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
* Automatic login via session or token authentication.


Requirements
------------

* Django >= 1.6
* Django REST Framework >= 2.4.3

Currently developed only for python 2.7.


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


License
-------

Django-REST-Assured is distributed under the BSD license.
