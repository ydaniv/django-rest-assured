0.2.0 (TBD)
-----------

*New:*

 - ``response_lookup_field`` attribute and corresponding ``get_lookup_from_response()`` to ``CreateAPITestCaseMixin`` for custom lookups of the created object in DB from the response data.

 - ``relationship_lookup_field`` attribute and corresponding ``get_relationship_value()`` to ``UpdateAPITestCaseMixin`` for custom lookups of related objects, e.g. when using a ``HyperlinkedRelatedField``.

 - Added missing kwargs in ``get_update_response()`` (Thanks, @sramana!).

 - Allow passing a dictionary to ``_update_check_db()`` for performing checks on serialized object.

 - ``data`` argument to ``TransitionAPITestCaseMixin.transition()`` to pass to ``client.post()`` as data.

*Changed:*

 - Updated support for Django 1.8 and Django REST Framework 3.1.

*Removed:*

 - Related objects with a ``uuid`` field are not looked up automatically anymore. Use the new ``relationship_lookup_field`` attribute and ``get_relationship_value()`` method.

0.1 (2014-12-21)
----------------

*New:*

 - First public stable version of Django-REST-Assured.
