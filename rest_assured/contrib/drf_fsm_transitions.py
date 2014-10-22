from rest_framework.reverse import reverse


class TransitionAPITestCaseMixin(object):

    """Adds the ``transition()`` method for testing state transition API endpoints.

    This is a handy extension for quickly test-covering API endpoints that are generated using
    the DRF-FSM-Transition library.
    """

    def transition(self, result, route, attribute='status'):

        """Send request to a transition view endpoint, verify and return the response.

        :param result: The expected value of the instance's ``attribute``.
        :param route: The addition to the route, usually the name of the transition action's name.
        :param attribute: Name of the instance's attribute that holds the state.
        :return: The view's response.
        """

        updateview = reverse(self.base_name + self.DETAIL_SUFFIX,
                             args=(self.object.pk,)) + '%s/' % route
        response = self.client.post(updateview)

        self.assertEqual(response.data[attribute], result)

        return response
