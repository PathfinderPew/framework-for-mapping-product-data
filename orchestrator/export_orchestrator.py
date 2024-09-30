# orchestrator/export_orchestrator.py

import pandas as pd
import logging
import os

def export_to_csv(df, filename='data_export.csv'):
    """
    Exports the given DataFrame to a CSV file.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing the data to export.
        filename (str): Name of the output CSV file. Default is 'data_export.csv'.
    
    Returns:
        bool: True if the export is successful, False otherwise.
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logging.info(f"Data exported to {filename} successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to export data to CSV: {e}")
        return False

def export_to_excel(df, filename='data_export.xlsx'):
    """
    Exports the given DataFrame to an Excel file.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing the data to export.
        filename (str): Name of the output Excel file. Default is 'data_export.xlsx'.
    
    Returns:
        bool: True if the export is successful, False otherwise.
    """
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        logging.info(f"Data exported to {filename} successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to export data to Excel: {e}")
        return False

def export_to_json(df, filename='data_export.json'):
    """
    Exports the given DataFrame to a JSON file.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing the data to export.
        filename (str): Name of the output JSON file. Default is 'data_export.json'.
    
    Returns:
        bool: True if the export is successful, False otherwise.
    """
    try:
        df.to_json(filename, orient='records', lines=True)
        logging.info(f"Data exported to {filename} successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to export data to JSON: {e}")
        return False

def select_export_format(df, format_type='csv', output_dir='exports'):
    """
    Orchestrates exporting the DataFrame based on the specified format type.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame to export.
        format_type (str): The format for exporting. Options are 'csv', 'excel', or 'json'. Default is 'csv'.
        output_dir (str): Directory to save the exported file. Default is 'exports'.
    
    Returns:
        bool: True if the export is successful, False otherwise.
    """
    # Ensure the export directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Determine filename based on format
    filename = os.path.join(output_dir, f"data_export.{format_type.lower()}")

    if format_type.lower() == 'csv':
        return export_to_csv(df, filename)
    elif format_type.lower() == 'excel':
        return export_to_excel(df, filename)
    elif format_type.lower() == 'json':
        return export_to_json(df, filename)
    else:
        logging.error(f"Unsupported export format: {format_type}. Supported formats are: 'csv', 'excel', 'json'.")
        return False
