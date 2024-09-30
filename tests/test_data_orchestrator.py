# tests/test_data_orchestrator.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import logging
from orchestrator.data_orchestrator import sync_netsuite_to_shopify

class TestDataOrchestrator(unittest.TestCase):
    @patch('orchestrator.data_orchestrator.shopify_adapter.upload_products')
    @patch('orchestrator.data_orchestrator.netsuite_adapter.fetch_netsuite_products')
    @patch('orchestrator.data_orchestrator.netsuite_mapping.map_to_shopify')
    def test_sync_netsuite_to_shopify_success(self, mock_map_to_shopify, mock_fetch_netsuite, mock_upload_products):
        """
        Test successful synchronization from NetSuite to Shopify.
        """
        # Arrange: Mock NetSuite data
        mock_netsuite_data = pd.DataFrame([{'title': 'Product A', 'price': 10.99}])
        mock_fetch_netsuite.return_value = mock_netsuite_data

        # Arrange: Mock mapped Shopify data
        mock_shopify_data = pd.DataFrame([{'Handle': 'product-a', 'Title': 'Product A', 'Price': 10.99}])
        mock_map_to_shopify.return_value = mock_shopify_data

        # Act: Call the orchestrator function
        sync_netsuite_to_shopify()

        # Assert: Verify that each step in the process was called with the correct data
        mock_fetch_netsuite.assert_called_once()
        mock_map_to_shopify.assert_called_once_with(mock_netsuite_data)
        mock_upload_products.assert_called_once_with(mock_shopify_data)

        # Optionally, assert the specific data passed to upload_products
        uploaded_data = mock_upload_products.call_args[0][0]
        pd.testing.assert_frame_equal(uploaded_data, mock_shopify_data, "The DataFrame passed to upload_products should match the mapped data.")

    @patch('orchestrator.data_orchestrator.logging')
    @patch('orchestrator.data_orchestrator.shopify_adapter.upload_products')
    @patch('orchestrator.data_orchestrator.netsuite_adapter.fetch_netsuite_products')
    @patch('orchestrator.data_orchestrator.netsuite_mapping.map_to_shopify')
    def test_sync_netsuite_to_shopify_empty_netsuite_data(self, mock_map_to_shopify, mock_fetch_netsuite, mock_upload_products, mock_logging):
        """
        Test sync_netsuite_to_shopify when no data is fetched from NetSuite.
        """
        # Arrange: Return an empty DataFrame from NetSuite
        mock_fetch_netsuite.return_value = pd.DataFrame()

        # Act: Call the orchestrator function
        sync_netsuite_to_shopify()

        # Assert: Check that mapping and upload are not called
        mock_map_to_shopify.assert_not_called()
        mock_upload_products.assert_not_called()

        # Assert: Verify warning log is captured
        mock_logging.warning.assert_called_once_with("No data fetched from NetSuite. Synchronization aborted.")

    @patch('orchestrator.data_orchestrator.logging')
    @patch('orchestrator.data_orchestrator.shopify_adapter.upload_products')
    @patch('orchestrator.data_orchestrator.netsuite_adapter.fetch_netsuite_products')
    @patch('orchestrator.data_orchestrator.netsuite_mapping.map_to_shopify')
    def test_sync_netsuite_to_shopify_empty_shopify_data(self, mock_map_to_shopify, mock_fetch_netsuite, mock_upload_products, mock_logging):
        """
        Test sync_netsuite_to_shopify when mapping to Shopify format results in an empty DataFrame.
        """
        # Arrange: Mock NetSuite data
        mock_netsuite_data = pd.DataFrame([{'title': 'Product A', 'price': 10.99}])
        mock_fetch_netsuite.return_value = mock_netsuite_data

        # Arrange: Return an empty DataFrame from mapping
        mock_map_to_shopify.return_value = pd.DataFrame()

        # Act: Call the orchestrator function
        sync_netsuite_to_shopify()

        # Assert: Verify that upload is not called
        mock_upload_products.assert_not_called()

        # Assert: Verify warning log is captured
        mock_logging.warning.assert_called_once_with("Mapping to Shopify format failed. No data to upload.")

    @patch('orchestrator.data_orchestrator.logging')
    @patch('orchestrator.data_orchestrator.shopify_adapter.upload_products')
    @patch('orchestrator.data_orchestrator.netsuite_adapter.fetch_netsuite_products')
    @patch('orchestrator.data_orchestrator.netsuite_mapping.map_to_shopify')
    def test_sync_netsuite_to_shopify_upload_failure(self, mock_map_to_shopify, mock_fetch_netsuite, mock_upload_products, mock_logging):
        """
        Test sync_netsuite_to_shopify when upload to Shopify fails.
        """
        # Arrange: Mock NetSuite data
        mock_netsuite_data = pd.DataFrame([{'title': 'Product A', 'price': 10.99}])
        mock_fetch_netsuite.return_value = mock_netsuite_data

        # Arrange: Mock mapped Shopify data
        mock_shopify_data = pd.DataFrame([{'Handle': 'product-a', 'Title': 'Product A', 'Price': 10.99}])
        mock_map_to_shopify.return_value = mock_shopify_data

        # Arrange: Mock upload failure
        mock_upload_products.return_value = False

        # Act: Call the orchestrator function
        sync_netsuite_to_shopify()

        # Assert: Verify that fetch, mapping, and upload are called
        mock_fetch_netsuite.assert_called_once()
        mock_map_to_shopify.assert_called_once_with(mock_netsuite_data)
        mock_upload_products.assert_called_once_with(mock_shopify_data)

        # Assert: Verify error log is captured
        mock_logging.error.assert_called_once_with("Data upload to Shopify failed.")

if __name__ == '__main__':
    unittest.main()
