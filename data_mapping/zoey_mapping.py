import pandas as pd
import logging
import os
import requests
from data_mapping.common_mapping import clean_html, normalize_column_names, fill_missing_values

# Fetch environment variables (API key)
from dotenv import load_dotenv
load_dotenv()

# Zoey API Key
ZOEY_API_KEY = os.getenv("ZOEY_API_KEY")

def fetch_data_from_zoey():
    """
    Fetch product data from Zoey API and return as a DataFrame.

    Returns:
        pandas.DataFrame: DataFrame containing product data from Zoey.
    """
    try:
        # Define the Zoey API endpoint for fetching products
        api_url = "https://api.zoey.com/v1/products"
        
        # Check for the API key
        if not ZOEY_API_KEY:
            logging.error("Zoey API key not found. Please set ZOEY_API_KEY in .env.")
            return pd.DataFrame()

        # Set up request headers
        headers = {
            "Authorization": f"Bearer {ZOEY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Make the API request to fetch product data
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            zoey_data = response.json()  # Parse the JSON response
            logging.info(f"Fetched {len(zoey_data)} products from Zoey via API.")
            return pd.json_normalize(zoey_data)  # Normalize nested JSON to a flat DataFrame

        else:
            logging.error(f"Failed to fetch data from Zoey: {response.status_code} - {response.text}")
            return pd.DataFrame()

    except Exception as err:
        logging.error(f"An error occurred while fetching data from Zoey: {err}")
        return pd.DataFrame()


def map_output_to_zoey_csv(df):
    """
    Maps data from other sources (NetSuite, Shopify) to Zoey's CSV format.

    Parameters:
        df (pandas.DataFrame): DataFrame containing product information.

    Returns:
        pandas.DataFrame: Mapped DataFrame ready for Zoey's CSV import.
    """
    try:
        # Step 1: Normalize the column names
        df = normalize_column_names(df)

        # Step 2: Clean the 'body_html' field if present
        if 'body_html' in df.columns:
            df['body_html'] = df['body_html'].apply(clean_html)

        # Step 3: Fill missing values
        df = fill_missing_values(df)

        # Step 4: Map columns to Zoey's CSV format based on the template
        zoey_csv_df = pd.DataFrame()
        zoey_csv_df['sku'] = df.get('sku', '')
        zoey_csv_df['_type'] = df.get('_type', 'simple')
        zoey_csv_df['name'] = df.get('title', '')
        zoey_csv_df['description'] = df.get('body_html', '')
        zoey_csv_df['price'] = df.get('variant_price', 0.0)
        zoey_csv_df['status'] = df.get('status', 1)
        zoey_csv_df['qty'] = df.get('variant_inventory_qty', 0)
        zoey_csv_df['visibility'] = df.get('visibility', 4)
        zoey_csv_df['use_config_manage_stock'] = df.get('use_config_manage_stock', 1)
        zoey_csv_df['is_in_stock'] = df.get('is_in_stock', 1)
        zoey_csv_df['manage_stock'] = df.get('manage_stock', 1)
        zoey_csv_df['tax_class_id'] = df.get('tax_class_id', 2)
        zoey_csv_df['weight'] = df.get('variant_weight_unit', 0.0)
        zoey_csv_df['barcode'] = df.get('barcode', '')
        zoey_csv_df['brand'] = df.get('brand', '')
        zoey_csv_df['color'] = df.get('color', '')
        zoey_csv_df['url_key'] = df.get('url_key', '')
        zoey_csv_df['image'] = df.get('image_src', '')
        zoey_csv_df['_media_image'] = df.get('image_src', '')
        zoey_csv_df['category_ids'] = df.get('category_ids', '')
        zoey_csv_df['use_config_enable_qty_inc'] = df.get('use_config_enable_qty_inc', 1)
        zoey_csv_df['enable_qty_increments'] = df.get('enable_qty_increments', 1)
        zoey_csv_df['use_config_qty_increments'] = df.get('use_config_qty_increments', 1)
        zoey_csv_df['qty_increments'] = df.get('qty_increments', 0)
        zoey_csv_df['zoey_add_to_cart_qty'] = df.get('zoey_add_to_cart_qty', 1)

        logging.info("Data mapping to Zoey's CSV format completed.")
        return zoey_csv_df

    except Exception as err:
        logging.error(f"An error occurred during mapping: {err}")
        return pd.DataFrame()


def generate_mock_zoey_csv(output_file='zoey_mock_data.csv'):
    """
    Generates a mock CSV file for Zoey based on the required column structure.

    Parameters:
        output_file (str): The name of the output CSV file.

    Returns:
        None
    """
    # Define the required columns as specified
    columns = [
        'sku', '_type', 'name', 'description', 'price', 'status', 'qty', 'visibility',
        'use_config_manage_stock', 'is_in_stock', 'manage_stock', 'tax_class_id',
        'weight', 'barcode', 'brand', 'color', 'url_key', 'image', '_media_image',
        'category_ids', 'use_config_enable_qty_inc', 'enable_qty_increments',
        'use_config_qty_increments', 'qty_increments', 'zoey_add_to_cart_qty'
    ]

    # Create mock data for each column
    mock_data = {
        'sku': ['SKU001', 'SKU002', 'SKU003'],
        '_type': ['simple', 'simple', 'configurable'],
        'name': ['Product A', 'Product B', 'Product C'],
        'description': ['Description of Product A', 'Description of Product B', 'Description of Product C'],
        'price': [10.99, 15.49, 0.0],
        'status': [1, 2, 1],
        'qty': [100, 50, 0],
        'visibility': [4, 4, 1],
        'use_config_manage_stock': [1, 1, 0],
        'is_in_stock': [1, 1, 0],
        'manage_stock': [1, 1, 0],
        'tax_class_id': [2, 2, 2],
        'weight': [0.5, 1.0, 0.0],
        'barcode': ['123456789012', '987654321098', ''],
        'brand': ['Brand A', 'Brand B', 'Brand C'],
        'color': ['Red', 'Blue', ''],
        'url_key': ['product-a', 'product-b', 'product-c'],
        'image': ['image_a.jpg', 'image_b.jpg', ''],
        '_media_image': ['image_a.jpg', 'image_b.jpg', 'image_c.jpg'],
        'category_ids': ['Shop/Accessories/Earrings', 'Shop/Apparel/Shirts', ''],
        'use_config_enable_qty_inc': [1, 1, 0],
        'enable_qty_increments': [1, 0, 0],
        'use_config_qty_increments': [1, 1, 0],
        'qty_increments': [1, 2, 0],
        'zoey_add_to_cart_qty': [1, 1, 0]
    }

    # Create a DataFrame using the mock data
    df = pd.DataFrame(mock_data, columns=columns)

    # Save to CSV
    df.to_csv(output_file, index=False)
    logging.info(f"Mock Zoey CSV file generated successfully: {output_file}")
