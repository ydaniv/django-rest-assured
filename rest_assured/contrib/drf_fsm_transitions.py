from rest_framework.reverse import reverse


class TransitionAPITestCaseMixin(object):

    """Adds the ``transition()`` method for testing state transition API endpoints.

    This is a handy extension for quickly test-covering API endpoints that are generated using
    the DRF-FSM-Transition library.
    """

    def transition(self, result, route, attribute='status', from_state=None, data=None):

        """Send request to a transition view endpoint, verify and return the response.

        :param result: The expected value of the instance's ``attribute``.
        :param route: The addition to the route, usually the name of the transition action's name.
        :param attribute: Name of the instance's attribute that holds the state.
        :param from_state: A state to update the object to, to initialize the "from" state.
        :return: The view's response.
        """

        if from_state is not None:
            self.object.__class__.objects.filter(pk=self.object.pk).update(**{attribute: from_state})

        updateview = reverse(self.base_name + self.DETAIL_SUFFIX,
                             args=(self.object.pk,)) + '%s/' % route
        response = self.client.post(updateview, data)

        self.assertEqual(response.data[attribute], result)

        return response
