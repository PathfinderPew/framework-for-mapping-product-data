# data_mapping/zoey_mapping.py

import pandas as pd
import logging
from data_mapping.common_mapping import clean_html, normalize_column_names, fill_missing_values

def map_output_to_zoey_csv(df):
    """
    Maps data from NetSuite or Shopify to Zoey's CSV format.

    Parameters:
        df (pandas.DataFrame): DataFrame containing product information.

    Returns:
        pandas.DataFrame: Mapped DataFrame ready for Zoey's CSV import.
    """
    # Step 1: Normalize the column names
    df = normalize_column_names(df)

    # Step 2: Clean the 'Body (HTML)' field if present
    if 'body_(html)' in df.columns:
        df['body_(html)'] = df['body_(html)'].apply(clean_html)

    # Step 3: Fill missing values
    df = fill_missing_values(df)

    # Step 4: Ensure all necessary columns are present
    if 'status' not in df.columns:
        df['status'] = 'active'

    # Step 5: Map columns to Zoey's CSV format based on the template
    zoey_csv_df = pd.DataFrame()
    zoey_csv_df['Handle'] = df['handle']
    zoey_csv_df['Title'] = df['title']
    zoey_csv_df['Description'] = df['body_(html)']
    zoey_csv_df['Vendor'] = df['vendor']
    zoey_csv_df['Type'] = df['type']
    zoey_csv_df['Tags'] = df['tags']
    zoey_csv_df['Published'] = df['published']
    zoey_csv_df['SKU'] = df['variant_sku']
    zoey_csv_df['Price'] = df['variant_price']
    zoey_csv_df['Inventory Quantity'] = df['variant_inventory_qty']
    zoey_csv_df['Barcode'] = df['variant_barcode']
    zoey_csv_df['Image URL'] = df['image_src']
    zoey_csv_df['Image Alt Text'] = df['image_alt_text']

    # Create 'Handle' from 'Title' if not already present
    zoey_csv_df['Handle'] = zoey_csv_df['Title'].str.lower().str.replace(' ', '-').str.replace('/', '-')

    # Ensure data types are correct
    zoey_csv_df['Published'] = zoey_csv_df['Published'].astype(bool)
    zoey_csv_df['Price'] = zoey_csv_df['Price'].astype(float)
    zoey_csv_df['Inventory Quantity'] = zoey_csv_df['Inventory Quantity'].astype(int)

    logging.info("Data mapping to Zoey's CSV format completed.")
    return zoey_csv_df
