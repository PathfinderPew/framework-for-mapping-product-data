# tests/test_shopify_adapter.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from adapters.shopify_adapter import fetch_shopify_data
from data_mapping.common_mapping import clean_html

class TestShopifyAdapter(unittest.TestCase):

    @patch('adapters.shopify_adapter.pd.read_excel')
    @patch('adapters.shopify_adapter.normalize_column_names')  
    @patch('adapters.shopify_adapter.clean_html')  
    def test_fetch_shopify_data_success(self, mock_clean_html, mock_normalize_column_names, mock_read_excel):
        # Arrange: Create a mock DataFrame to be returned by read_excel
        mock_data = {
            'variant_price': [10.99, 15.99, None],
            'variant_sku': ['SKU001', 'SKU002', 'SKU003'],
            'title': ['Product A', 'Product B', 'Product C'],
            'body_(html)': ['<p>Desc A</p>', '<p>Desc B</p>', None],
            'variant_inventory_qty': [100, 200, 300]
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df

        # Mock normalized column names to return the mock DataFrame itself
        mock_normalize_column_names.return_value = mock_df

        # Mock the `clean_html` function to simulate HTML cleaning
        mock_clean_html.side_effect = lambda x: x.replace('<p>', '').replace('</p>', '') if x else ''

        # Act: Call the function
        result_df = fetch_shopify_data('Test Shopify Sheet.xlsx')

        # Assert: Verify that read_excel was called correctly with the specified file
        mock_read_excel.assert_called_once_with('Test Shopify Sheet.xlsx', engine='openpyxl')

        # Assert: Verify that `normalize_column_names` was called on the read DataFrame
        mock_normalize_column_names.assert_called_once()

        # Assert: Verify that `clean_html` was called three times (one for each HTML entry)
        self.assertEqual(mock_clean_html.call_count, 3, "The `clean_html` function should be called three times.")

        # Assert: Check the resulting DataFrame structure and content
        self.assertFalse(result_df.empty, "The resulting DataFrame should not be empty.")
        self.assertEqual(len(result_df), 3, "The resulting DataFrame should have 3 rows.")
        self.assertIn('variant_sku', result_df.columns, "The 'variant_sku' column should be present after normalization.")
        self.assertEqual(result_df.loc[0, 'variant_price'], 10.99, "Variant Price should be correctly parsed.")
        self.assertEqual(result_df.loc[2, 'variant_price'], 0.0, "Missing Variant Price should be filled with 0.")
        self.assertEqual(result_df.loc[0, 'body_(html)'], 'Desc A', "HTML tags should be removed from the description.")
        self.assertEqual(result_df.loc[2, 'body_(html)'], '', "Missing Description should be filled with an empty string.")

    @patch('adapters.shopify_adapter.pd.read_excel')
    def test_fetch_shopify_data_file_not_found(self, mock_read_excel):
        # Arrange: Configure read_excel to raise FileNotFoundError
        mock_read_excel.side_effect = FileNotFoundError

        # Act: Call the function with a nonexistent file
        with self.assertLogs('adapters.shopify_adapter', level='ERROR') as log:
            result_df = fetch_shopify_data('Nonexistent File.xlsx')

        # Assert: Verify that an empty DataFrame is returned
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty when the file is not found.")
        self.assertEqual(len(result_df), 0, "The resulting DataFrame should have 0 rows when the file is not found.")

        # Assert: Check if the correct error message is logged
        self.assertIn("The file 'Nonexistent File.xlsx' was not found.", log.output[0])

    @patch('adapters.shopify_adapter.pd.read_excel')
    def test_fetch_shopify_data_general_exception(self, mock_read_excel):
        # Arrange: Configure read_excel to raise a generic Exception
        mock_read_excel.side_effect = Exception("General Error")

        # Act: Call the function to simulate an error during Excel reading
        with self.assertLogs('adapters.shopify_adapter', level='ERROR') as log:
            result_df = fetch_shopify_data('Test Shopify Sheet.xlsx')

        # Assert: Verify that an empty DataFrame is returned
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty when a general exception occurs.")
        self.assertEqual(len(result_df), 0, "The resulting DataFrame should have 0 rows when an exception occurs.")

        # Assert: Check if the correct error message is logged
        self.assertIn("An error occurred while processing 'Test Shopify Sheet.xlsx': General Error", log.output[0])

if __name__ == '__main__':
    unittest.main()
