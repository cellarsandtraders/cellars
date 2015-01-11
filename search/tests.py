import json
import mock
from mock import Mock

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(BREWERYDB_BASEURI='http://example.com')
    @mock.patch('utils.brewerydb.requests')
    def test_successful_search(self, mock_requests):
        mock_requests.get.return_value = mock_response = Mock()
        mock_response.json.return_value = {"status": "success", "data": []}
        query = "Big Hugs"
        response = self.client.get(
            reverse('search'),
            {'q': query}
        )

        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue('status' in response_data)
        self.assertTrue('data' in response_data)

    def test_bad_request(self):
        response = self.client.get(reverse('search'), {})
        self.assertEqual(response.status_code, 400)
