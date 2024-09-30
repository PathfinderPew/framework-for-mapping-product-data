# tests/test_netsuite_adapter.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from adapters.netsuite_adapter import fetch_netsuite_products
import requests

class TestNetSuiteAdapter(unittest.TestCase):
    @patch('adapters.netsuite_adapter.make_request')  # Mock `make_request` from `common_adapter`
    @patch('adapters.netsuite_adapter.os.getenv')
    def test_fetch_netsuite_products_success(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_access_token'

        # Mock API responses for pagination
        first_response = MagicMock()
        first_response.status_code = 200
        first_response.json.return_value = {
            'items': [
                {'title': 'Product A', 'variant price': 10.99, 'variant sku': 'SKU001'},
                {'title': 'Product B', 'variant price': 15.99, 'variant sku': 'SKU002'}
            ]
        }

        second_response = MagicMock()
        second_response.status_code = 200
        second_response.json.return_value = {'items': []}

        # Configure the side effect of make_request to simulate pagination
        mock_make_request.side_effect = [first_response, second_response]

        # Act: Call the function
        result_df = fetch_netsuite_products()

        # Assert: Verify that make_request was called twice (pagination)
        self.assertEqual(mock_make_request.call_count, 2, "Should make two API calls for pagination.")

        # Assert: Check the content of the returned DataFrame
        expected_data = {
            'title': ['Product A', 'Product B'],
            'variant price': [10.99, 15.99],
            'variant sku': ['SKU001', 'SKU002']
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df)

    @patch('adapters.netsuite_adapter.make_request')  # Mock `make_request`
    @patch('adapters.netsuite_adapter.os.getenv')
    def test_fetch_netsuite_products_http_error(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_access_token'

        # Mock make_request to raise HTTPError
        mock_make_request.side_effect = requests.exceptions.HTTPError("404 Client Error")

        # Act & Assert: Expect the function to catch the error and return an empty DataFrame
        result_df = fetch_netsuite_products()
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty on HTTPError.")

    @patch('adapters.netsuite_adapter.make_request')  # Mock `make_request`
    @patch('adapters.netsuite_adapter.os.getenv')
    def test_fetch_netsuite_products_connection_error(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_access_token'

        # Configure make_request to raise a ConnectionError
        mock_make_request.side_effect = requests.exceptions.ConnectionError("Failed to establish a new connection")

        # Act & Assert: Expect the function to catch the error and return an empty DataFrame
        result_df = fetch_netsuite_products()
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty on ConnectionError.")

    @patch('adapters.netsuite_adapter.make_request')  # Mock `make_request`
    @patch('adapters.netsuite_adapter.os.getenv')
    def test_fetch_netsuite_products_missing_access_token(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable to return None
        mock_getenv.return_value = None

        # Act: Call the function
        result_df = fetch_netsuite_products()

        # Assert: Verify that make_request was never called
        mock_make_request.assert_not_called()

        # Assert: Check that an empty DataFrame is returned
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty when access token is missing.")

if __name__ == '__main__':
    unittest.main()
