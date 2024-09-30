# tests/test_shopify_adapter.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from adapters.shopify_adapter import fetch_shopify_data
from data_mapping.common_mapping import clean_html

class TestShopifyAdapter(unittest.TestCase):
    @patch('adapters.shopify_adapter.pd.read_excel')
    @patch('adapters.shopify_adapter.normalize_column_names')  # Mock `normalize_column_names`
    @patch('adapters.shopify_adapter.clean_html')  # Mock `clean_html`
    def test_fetch_shopify_data_success(self, mock_clean_html, mock_normalize_column_names, mock_read_excel):
        # Arrange: Create a mock DataFrame to be returned by read_excel
        mock_data = {
            'Variant Price': [10.99, 15.99, None],
            'Variant SKU': ['SKU001', 'SKU002', 'SKU003'],
            'Title': ['Product A', 'Product B', 'Product C'],
            'Body (HTML)': ['<p>Desc A</p>', '<p>Desc B</p>', None],
            'Variant Inventory Qty': [100, 200, 300]
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df

        # Mock normalized column names
        normalized_columns = mock_df.columns.str.lower().str.replace(' ', '_').str.replace('(', '_').str.replace(')', '')
        mock_normalize_column_names.return_value = mock_df.rename(columns=dict(zip(mock_df.columns, normalized_columns)))

        # Mock the `clean_html` function to simulate HTML cleaning
        mock_clean_html.side_effect = lambda x: x.replace('<p>', '').replace('</p>', '') if x else ''

        # Act: Call the function
        result_df = fetch_shopify_data('Test Shopify Sheet.xlsx')

        # Assert: Verify that read_excel was called correctly
        mock_read_excel.assert_called_once_with('Test Shopify Sheet.xlsx', engine='openpyxl')

        # Assert: Verify that `normalize_column_names` was called
        mock_normalize_column_names.assert_called_once()

        # Assert: Verify that `clean_html` was called for each row in the 'Body (HTML)' column
        self.assertEqual(mock_clean_html.call_count, 3, "The `clean_html` function should be called three times.")

        # Assert: Check that the DataFrame is processed correctly
        self.assertFalse(result_df.empty, "The resulting DataFrame should not be empty.")
        self.assertEqual(len(result_df), 3, "The resulting DataFrame should have 3 rows.")
        self.assertIn('variant_sku', result_df.columns, "The 'variant_sku' column should be present after normalization.")
        self.assertEqual(result_df.loc[0, 'variant_price'], 10.99, "Variant Price should be correctly parsed.")
        self.assertEqual(result_df.loc[2, 'variant_price'], 0.0, "Missing Variant Price should be filled with 0.")
        self.assertEqual(result_df.loc[0, 'body_(html)'], 'Desc A', "HTML tags should be removed from Description.")
        self.assertEqual(result_df.loc[2, 'body_(html)'], '', "Missing Description should be filled with an empty string.")

    @patch('adapters.shopify_adapter.pd.read_excel')
    def test_fetch_shopify_data_file_not_found(self, mock_read_excel):
        # Arrange: Configure read_excel to raise FileNotFoundError
        mock_read_excel.side_effect = FileNotFoundError

        # Act: Call the function
        result_df = fetch_shopify_data('Nonexistent File.xlsx')

        # Assert: Verify that an empty DataFrame is returned
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty when file is not found.")

    @patch('adapters.shopify_adapter.pd.read_excel')
    def test_fetch_shopify_data_general_exception(self, mock_read_excel):
        # Arrange: Configure read_excel to raise a generic Exception
        mock_read_excel.side_effect = Exception("General Error")

        # Act: Call the function
        result_df = fetch_shopify_data('Test Shopify Sheet.xlsx')

        # Assert: Verify that an empty DataFrame is returned
        self.assertTrue(result_df.empty, "The resulting DataFrame should be empty when a general exception occurs.")

if __name__ == '__main__':
    unittest.main()
