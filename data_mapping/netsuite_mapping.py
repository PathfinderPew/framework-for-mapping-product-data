# data_mapping/netsuite_mapping.py

import pandas as pd
import logging

def map_to_shopify(netsuite_df):
    """
    Maps NetSuite product data to the format required for Shopify.

    Parameters:
        netsuite_df (pandas.DataFrame): DataFrame containing product data from NetSuite.

    Returns:
        pandas.DataFrame: Mapped DataFrame formatted for Shopify.
    """
    try:
        # Handle missing columns and map NetSuite columns to Shopify columns
        shopify_df = pd.DataFrame()
        shopify_df['Handle'] = netsuite_df.get('title', pd.Series()).str.lower().str.replace(' ', '-').str.replace('/', '-')
        shopify_df['Title'] = netsuite_df.get('title', '')
        shopify_df['Body (HTML)'] = netsuite_df.get('description', '')  # Use description or empty if not present
        shopify_df['Vendor'] = netsuite_df.get('vendor', 'Unknown')
        shopify_df['Type'] = netsuite_df.get('type', 'Product')
        shopify_df['Tags'] = netsuite_df.get('tags', '')
        shopify_df['Published'] = True
        shopify_df['Variant SKU'] = netsuite_df.get('variant sku', '')
        shopify_df['Variant Price'] = netsuite_df.get('variant price', 0.0).fillna(0.0)  # Fill NaN values with 0.0
        shopify_df['Variant Inventory Qty'] = netsuite_df.get('inventory_qty', 0).fillna(0)  # Ensure no NaN in inventory
        shopify_df['Variant Barcode'] = netsuite_df.get('barcode', '')

        # Log the mapping details
        logging.info(f"Mapping {len(shopify_df)} products from NetSuite to Shopify format completed successfully.")
        return shopify_df

    except KeyError as e:
        logging.error(f"KeyError during NetSuite to Shopify mapping: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    except Exception as err:
        logging.error(f"An unexpected error occurred during NetSuite to Shopify mapping: {err}")
        return pd.DataFrame()


def map_to_zoey(netsuite_df):
    """
    Maps NetSuite product data to the format required for Zoey.

    Parameters:
        netsuite_df (pandas.DataFrame): DataFrame containing product data from NetSuite.

    Returns:
        pandas.DataFrame: Mapped DataFrame formatted for Zoey.
    """
    try:
        # Handle missing columns and map NetSuite columns to Zoey columns
        zoey_df = pd.DataFrame()
        zoey_df['Handle'] = netsuite_df.get('title', pd.Series()).str.lower().str.replace(' ', '-').str.replace('/', '-')
        zoey_df['Title'] = netsuite_df.get('title', '')
        zoey_df['Description'] = netsuite_df.get('description', '')
        zoey_df['Vendor'] = netsuite_df.get('vendor', 'Unknown')
        zoey_df['Type'] = netsuite_df.get('type', 'Product')
        zoey_df['Tags'] = netsuite_df.get('tags', '')
        zoey_df['Published'] = True
        zoey_df['SKU'] = netsuite_df.get('variant sku', '')
        zoey_df['Price'] = netsuite_df.get('variant price', 0.0).fillna(0.0)  # Fill NaN values with 0.0
        zoey_df['Inventory Quantity'] = netsuite_df.get('inventory_qty', 0).fillna(0)  # Ensure no NaN in inventory
        zoey_df['Barcode'] = netsuite_df.get('barcode', '')
        zoey_df['Image URL'] = netsuite_df.get('image_url', '')
        zoey_df['Image Alt Text'] = netsuite_df.get('image_alt_text', '')

        # Log the mapping details
        logging.info(f"Mapping {len(zoey_df)} products from NetSuite to Zoey format completed successfully.")
        return zoey_df

    except KeyError as e:
        logging.error(f"KeyError during NetSuite to Zoey mapping: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    except Exception as err:
        logging.error(f"An unexpected error occurred during NetSuite to Zoey mapping: {err}")
        return pd.DataFrame()
