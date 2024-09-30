import pandas as pd
import logging
from dotenv import load_dotenv
import os
from data_mapping.common_mapping import clean_html, normalize_column_names

# Load environment variables
load_dotenv()

def fetch_shopify_data(file='Test Shopify Sheet.xlsx'):
    """
    Fetches product data from a Shopify-formatted Excel file and ensures data compatibility.
    
    Parameters:
        file (str): The path to the Shopify Excel file.
    
    Returns:
        pandas.DataFrame: Cleaned and processed product data.
    """
    try:
        # Step 1: Read data from the Excel file
        output_df = pd.read_excel(file, engine='openpyxl')
        logging.info(f"Data successfully read from {file}")
        
        # Step 2: Normalize column names to handle inconsistencies in formatting
        output_df = normalize_column_names(output_df)

        # Optional: Log column names for verification
        logging.debug(f"Columns in DataFrame after normalization: {output_df.columns.tolist()}")

        # Step 3: Ensure 'variant_price' is numeric and handle errors
        if 'variant_price' in output_df.columns:
            output_df['variant_price'] = pd.to_numeric(output_df['variant_price'], errors='coerce')
        else:
            logging.warning("Column 'variant_price' not found. Creating with default values of 0.")
            output_df['variant_price'] = 0

        # Step 4: Ensure key columns are of correct data types and handle missing columns
        required_columns = {'variant_sku', 'title', 'body_(html)'}
        missing_columns = required_columns - set(output_df.columns)

        for col in missing_columns:
            logging.warning(f"Column '{col}' is missing. Creating with default values.")
            if col == 'body_(html)':
                output_df[col] = ''  # Create an empty HTML column for missing descriptions
            else:
                output_df[col] = 'N/A'  # Default placeholder for SKU and Title

        output_df['variant_sku'] = output_df['variant_sku'].astype(str)
        output_df['title'] = output_df['title'].astype(str)
        output_df['body_(html)'] = output_df['body_(html)'].apply(clean_html)

        # Step 5: Handle missing data by dropping rows without mandatory fields
        output_df.dropna(subset=['variant_sku', 'title'], inplace=True)
        
        # Fill missing 'variant_price' values with 0 (after conversion to numeric)
        output_df['variant_price'] = output_df['variant_price'].fillna(0)

        # Fill missing 'body_(html)' with an empty string
        output_df['body_(html)'] = output_df['body_(html)'].fillna('')

        # Step 6: Reset the index after cleaning the data
        output_df.reset_index(drop=True, inplace=True)

        # Optional: Log data types and a preview for verification
        logging.debug(f"Data types after processing:\n{output_df.dtypes}")
        logging.debug(f"First few rows of processed data:\n{output_df.head()}")

        # Return the cleaned and formatted DataFrame
        return output_df

    except FileNotFoundError:
        logging.error(f"The file '{file}' was not found. Please check the file path and name.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"An error occurred while processing '{file}': {e}")
        return pd.DataFrame()
