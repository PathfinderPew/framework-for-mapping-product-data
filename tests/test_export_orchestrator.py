# tests/test_export_orchestrator.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from orchestrator.export_orchestrator import export_to_csv, export_to_excel, export_to_json, select_export_format

class TestExportOrchestrator(unittest.TestCase):
    @patch('orchestrator.export_orchestrator.pd.DataFrame.to_csv')
    def test_export_to_csv_success(self, mock_to_csv):
        mock_to_csv.return_value = None
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        result = export_to_csv(df, filename='test_export.csv')
        self.assertTrue(result)
        mock_to_csv.assert_called_once()

    @patch('orchestrator.export_orchestrator.pd.ExcelWriter')
    def test_export_to_excel_success(self, mock_excel_writer):
        # Simulate successful behavior of the ExcelWriter context manager
        mock_writer_instance = MagicMock()
        mock_excel_writer.return_value = mock_writer_instance
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        result = export_to_excel(df, filename='test_export.xlsx')
        
        # Assertions for mock interactions and function success
        self.assertTrue(result)
        mock_excel_writer.assert_called_once()
        mock_writer_instance.__enter__.assert_called_once()
        mock_writer_instance.__exit__.assert_called_once()

    @patch('orchestrator.export_orchestrator.pd.DataFrame.to_json')
    def test_export_to_json_success(self, mock_to_json):
        mock_to_json.return_value = None
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        result = export_to_json(df, filename='test_export.json')
        self.assertTrue(result)
        mock_to_json.assert_called_once()

    @patch('orchestrator.export_orchestrator.export_to_csv')
    def test_select_export_format_csv(self, mock_export_to_csv):
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        select_export_format(df, format_type='csv')
        mock_export_to_csv.assert_called_once()

if __name__ == '__main__':
    unittest.main()
