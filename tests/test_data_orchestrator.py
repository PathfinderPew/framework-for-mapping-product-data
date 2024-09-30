# tests/test_data_orchestrator.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from orchestrator.data_orchestrator import sync_netsuite_to_shopify

class TestDataOrchestrator(unittest.TestCase):
    @patch('orchestrator.data_orchestrator.shopify_adapter.upload_products')
    @patch('orchestrator.data_orchestrator.netsuite_adapter.fetch_netsuite_products')
    @patch('orchestrator.data_orchestrator.netsuite_mapping.map_to_shopify')
    def test_sync_netsuite_to_shopify(self, mock_map_to_shopify, mock_fetch_netsuite, mock_upload_products):
        # Arrange: Mock NetSuite data
        mock_netsuite_data = pd.DataFrame([{'title': 'Product A', 'price': 10.99}])
        mock_fetch_netsuite.return_value = mock_netsuite_data

        # Arrange: Mock mapped Shopify data
        mock_shopify_data = pd.DataFrame([{'Handle': 'product-a', 'Title': 'Product A', 'Price': 10.99}])
        mock_map_to_shopify.return_value = mock_shopify_data

        # Act: Call the orchestrator function
        sync_netsuite_to_shopify()

        # Assert: Check each step in the process
        mock_fetch_netsuite.assert_called_once()
        mock_map_to_shopify.assert_called_once_with(mock_netsuite_data)
        mock_upload_products.assert_called_once_with(mock_shopify_data)

        # Optionally, assert the specific data passed to upload_products
        uploaded_data = mock_upload_products.call_args[0][0]
        pd.testing.assert_frame_equal(uploaded_data, mock_shopify_data, 
                                      "The DataFrame passed to upload_products should match the mapped data.")

if __name__ == '__main__':
    unittest.main()
