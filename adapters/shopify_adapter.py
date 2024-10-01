# adapters/shopify_adapter.py

import pandas as pd
import logging
from dotenv import load_dotenv
import os
from data_mapping.common_mapping import clean_html, normalize_column_names

# Load environment variables
load_dotenv()

def fetch_shopify_data(file='Test Shopify Sheet.xlsx'):
    """
    Fetches and processes product data from a Shopify-formatted Excel file.
    
    Parameters:
        file (str): The path to the Shopify Excel file. Default is 'Test Shopify Sheet.xlsx'.
    
    Returns:
        pandas.DataFrame: A cleaned and processed DataFrame containing product data formatted for Shopify.
    """
    try:
        # Step 1: Read data from the Excel file using `openpyxl` engine
        output_df = pd.read_excel(file, engine='openpyxl')
        logging.info(f"Data successfully read from {file}")

        # Step 2: Normalize column names to ensure consistency across the DataFrame
        output_df = normalize_column_names(output_df)
        logging.debug(f"Columns in DataFrame after normalization: {output_df.columns.tolist()}")

        # Step 3: Ensure 'variant_price' column exists and is numeric
        if 'variant_price' in output_df.columns:
            output_df['variant_price'] = pd.to_numeric(output_df['variant_price'], errors='coerce')
        else:
            logging.warning("Column 'variant_price' not found. Creating with default values of 0.")
            output_df['variant_price'] = 0

        # Step 4: Check and create missing required columns with default values
        required_columns = {'variant_sku', 'title', 'body_(html)'}
        missing_columns = required_columns - set(output_df.columns)

        for col in missing_columns:
            logging.warning(f"Column '{col}' is missing. Creating with default values.")
            if col == 'body_(html)':
                output_df[col] = ''  # Default to an empty string for HTML descriptions
            else:
                output_df[col] = 'N/A'  # Default placeholder for SKU and Title

        # Step 5: Ensure data types are consistent and clean HTML in 'body_(html)'
        output_df['variant_sku'] = output_df['variant_sku'].astype(str)
        output_df['title'] = output_df['title'].astype(str)
        output_df['body_(html)'] = output_df['body_(html)'].apply(lambda x: clean_html(x) if isinstance(x, str) else '')

        # Step 6: Handle missing data by removing rows without mandatory fields
        output_df.dropna(subset=['variant_sku', 'title'], inplace=True)

        # Fill missing 'variant_price' values with 0 after conversion to numeric
        output_df['variant_price'] = output_df['variant_price'].fillna(0)

        # Ensure 'body_(html)' has no null values
        output_df['body_(html)'] = output_df['body_(html)'].fillna('')

        # Step 7: Reset index for a cleaner output DataFrame
        output_df.reset_index(drop=True, inplace=True)

        # Optional: Log a summary of the processed data for verification
        logging.debug(f"Data types after processing:\n{output_df.dtypes}")
        logging.debug(f"First few rows of processed data:\n{output_df.head()}")

        logging.info("Shopify data processed successfully.")
        return output_df

    except FileNotFoundError:
        logging.error(f"The file '{file}' was not found. Please check the file path and name.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logging.error(f"The file '{file}' is empty or does not contain valid data.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"An error occurred while processing '{file}': {e}")
        return pd.DataFrame()


def upload_products(df):
    """
    Mock function to upload products to Shopify.

    Parameters:
        df (pd.DataFrame): DataFrame containing the product information to be uploaded.

    Returns:
        bool: True if upload is successful, False otherwise.
    """
    if df.empty:
        logging.warning("No data to upload to Shopify. Please provide a valid DataFrame.")
        return False

    try:
        # Simulate the upload process
        logging.info(f"Uploading {len(df)} products to Shopify.")
        
        # Normally, the API request would be sent here (e.g., using requests.post())
        # Simulating success with logging
        logging.info("Products successfully uploaded to Shopify.")
        return True

    except Exception as err:
        logging.error(f"Failed to upload products to Shopify: {err}")
        return False
