0.2.1 (2017-21-21)
------------------

*Fixed:*

 - Fixed bug that caused attribute checks in ``test_detail`` with callables in ``attributes_to_check`` to fail.

*Removed:*

 - Official support for Python 3.2 since it's not supported by py.test.

0.2.0 (2015-11-27)
------------------

*Support:*

 - Updated support and now also tested against Django 1.8, and DRF 3.1, 3.2 and 3.3.

*Breaking:*

 - A new ``pagination_results_field`` attribute on the ``ListAPITestCaseMixin`` that controls the name of the key the result set is nested under. This was previously hardcoded to ``'results'`` but now defaults to ``None``, which means the test assumes pagination is turned off.

*New:*

 - ``response_lookup_field`` attribute and corresponding ``get_lookup_from_response()`` to ``CreateAPITestCaseMixin`` for custom lookups of the created object in DB from the response data.

 - ``relationship_lookup_field`` attribute and corresponding ``get_relationship_value()`` to ``UpdateAPITestCaseMixin`` for custom lookups of related objects, e.g. when using a ``HyperlinkedRelatedField``.

 - Added missing kwargs in ``get_update_response()`` (Thanks, @sramana!).

 - Allow passing a dictionary to ``_update_check_db()`` for performing checks on serialized object.

 - ``data`` argument to ``TransitionAPITestCaseMixin.transition()`` to pass to ``client.post()`` as data.

*Removed:*

 - Related objects with a ``uuid`` field are not looked up automatically anymore. Use the new ``relationship_lookup_field`` attribute and ``get_relationship_value()`` method.

0.1 (2014-12-21)
----------------

*New:*

 - First public stable version of Django-REST-Assured.
