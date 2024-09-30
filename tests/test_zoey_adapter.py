# tests/test_zoey_adapter.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from adapters.zoey_adapter import export_to_zoey  # Updated import

class TestZoeyAdapter(unittest.TestCase):  # Renamed class to match the file
    @patch('adapters.zoey_adapter.make_request')  # Updated `make_request` reference
    @patch('adapters.zoey_adapter.os.getenv')  # Updated reference for `os.getenv`
    def test_export_to_zoey_success(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_zoey_api_key'

        # Create a sample DataFrame
        data = {
            'Handle': ['product-a'],
            'Title': ['Product A'],
            'Description': ['Description for Product A'],
            'Vendor': ['Vendor A'],
            'Type': ['Type A'],
            'Tags': ['tag1, tag2'],
            'Published': [True],
            'SKU': ['SKU001'],
            'Price': [19.99],
            'Inventory Quantity': [100],
            'Barcode': ['1234567890123'],
            'Image URL': ['http://example.com/image_a.jpg'],
            'Image Alt Text': ['Image A']
        }
        df = pd.DataFrame(data)

        # Mock successful API response
        mock_make_request.return_value = MagicMock(status_code=201)

        # Act: Call the function
        success = export_to_zoey(df)

        # Assert: Verify that `make_request` was called correctly
        expected_api_url = "https://api.zoey.com/v1/products"
        mock_make_request.assert_called_once_with(
            "POST",
            expected_api_url,
            headers={
                "Authorization": f"Bearer {'valid_zoey_api_key'}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={
                "handle": 'product-a',
                "title": 'Product A',
                "description": 'Description for Product A',
                "vendor": 'Vendor A',
                "type": 'Type A',
                "tags": 'tag1, tag2',
                "published": True,
                "variants": [
                    {
                        "sku": 'SKU001',
                        "price": 19.99,
                        "inventory_quantity": 100,
                        "barcode": '1234567890123',
                    }
                ],
                "images": [
                    {
                        "src": 'http://example.com/image_a.jpg',
                        "alt_text": 'Image A'
                    }
                ],
            }
        )

        # Assert: Function should return True
        self.assertTrue(success, "Export to Zoey should return True on successful export.")

    @patch('adapters.zoey_adapter.make_request')  # Updated reference for `make_request`
    @patch('adapters.zoey_adapter.os.getenv')
    def test_export_to_zoey_failure(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_zoey_api_key'

        # Create a sample DataFrame with multiple products
        data = {
            'Handle': ['product-a', 'product-b'],
            'Title': ['Product A', 'Product B'],
            'Description': ['Description A', 'Description B'],
            'Vendor': ['Vendor A', 'Vendor B'],
            'Type': ['Type A', 'Type B'],
            'Tags': ['tag1, tag2', 'tag3, tag4'],
            'Published': [True, False],
            'SKU': ['SKU001', 'SKU002'],
            'Price': [19.99, 29.99],
            'Inventory Quantity': [100, 200],
            'Barcode': ['1234567890123', '9876543210987'],
            'Image URL': ['http://example.com/image_a.jpg', 'http://example.com/image_b.jpg'],
            'Image Alt Text': ['Image A', 'Image B']
        }
        df = pd.DataFrame(data)

        # Mock API response for the first product as success and the second as failure
        mock_make_request.side_effect = [MagicMock(status_code=201), None]  # Second call fails

        # Act: Call the function
        success = export_to_zoey(df)

        # Assert: Verify that make_request was called twice
        self.assertEqual(mock_make_request.call_count, 2, "Should make two API calls for two products.")

        # Assert: Function should return False due to the second export failure
        self.assertFalse(success, "Export to Zoey should return False if any export fails.")

    @patch('adapters.zoey_adapter.make_request')  # Updated reference for `make_request`
    @patch('adapters.zoey_adapter.os.getenv')
    def test_export_to_zoey_missing_api_key(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable to return None
        mock_getenv.return_value = None

        # Create a sample DataFrame
        data = {
            'Handle': ['product-a'],
            'Title': ['Product A'],
            'Description': ['Description A'],
            'Vendor': ['Vendor A'],
            'Type': ['Type A'],
            'Tags': ['tag1, tag2'],
            'Published': [True],
            'SKU': ['SKU001'],
            'Price': [19.99],
            'Inventory Quantity': [100],
            'Barcode': ['1234567890123'],
            'Image URL': ['http://example.com/image_a.jpg'],
            'Image Alt Text': ['Image A']
        }
        df = pd.DataFrame(data)

        # Act: Call the function
        success = export_to_zoey(df)

        # Assert: Verify that `make_request` was never called
        mock_make_request.assert_not_called()

        # Assert: Function should return False
        self.assertFalse(success, "Export to Zoey should return False when API key is missing.")

    @patch('adapters.zoey_adapter.make_request')  # Updated reference for `make_request`
    @patch('adapters.zoey_adapter.os.getenv')
    def test_export_to_zoey_http_error(self, mock_getenv, mock_make_request):
        # Arrange: Mock environment variable
        mock_getenv.return_value = 'valid_zoey_api_key'

        # Mock API response with HTTP error (return None)
        mock_make_request.return_value = None

        # Create a sample DataFrame
        data = {
            'Handle': ['product-a'],
            'Title': ['Product A'],
            'Description': ['Description A'],
            'Vendor': ['Vendor A'],
            'Type': ['Type A'],
            'Tags': ['tag1, tag2'],
            'Published': [True],
            'SKU': ['SKU001'],
            'Price': [19.99],
            'Inventory Quantity': [100],
            'Barcode': ['1234567890123'],
            'Image URL': ['http://example.com/image_a.jpg'],
            'Image Alt Text': ['Image A']
        }
        df = pd.DataFrame(data)

        # Act: Call the function
        success = export_to_zoey(df)

        # Assert: Verify that `make_request` was called once
        mock_make_request.assert_called_once()

        # Assert: Function should return False due to HTTP error
        self.assertFalse(success, "Export to Zoey should return False on HTTP error.")

if __name__ == '__main__':
    unittest.main()
