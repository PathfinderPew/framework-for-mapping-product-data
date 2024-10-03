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
        # Convert all columns to pandas.Series to handle missing values correctly
        shopify_df = pd.DataFrame()
        shopify_df['Handle'] = pd.Series(netsuite_df.get('title', '')).str.lower().str.replace(' ', '-').str.replace('/', '-')
        shopify_df['Title'] = pd.Series(netsuite_df.get('title', ''))
        shopify_df['Body (HTML)'] = pd.Series(netsuite_df.get('description', ''))  # Use description or empty if not present
        shopify_df['Vendor'] = pd.Series(netsuite_df.get('vendor', 'Unknown'))
        shopify_df['Type'] = pd.Series(netsuite_df.get('type', 'Product'))
        shopify_df['Tags'] = pd.Series(netsuite_df.get('tags', ''))
        shopify_df['Published'] = pd.Series([True] * len(shopify_df))
        shopify_df['Variant SKU'] = pd.Series(netsuite_df.get('variant sku', ''))
        shopify_df['Variant Price'] = pd.Series(netsuite_df.get('variant price', 0.0)).fillna(0.0)  # Fill NaN values with 0.0
        shopify_df['Variant Inventory Qty'] = pd.Series(netsuite_df.get('inventory_qty', 0)).fillna(0)  # Ensure no NaN in inventory
        shopify_df['Variant Barcode'] = pd.Series(netsuite_df.get('barcode', ''))

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
        # Convert all columns to pandas.Series to handle missing values correctly
        zoey_df = pd.DataFrame()
        zoey_df['Handle'] = pd.Series(netsuite_df.get('title', '')).str.lower().str.replace(' ', '-').str.replace('/', '-')
        zoey_df['Title'] = pd.Series(netsuite_df.get('title', ''))
        zoey_df['Description'] = pd.Series(netsuite_df.get('description', ''))
        zoey_df['Vendor'] = pd.Series(netsuite_df.get('vendor', 'Unknown'))
        zoey_df['Type'] = pd.Series(netsuite_df.get('type', 'Product'))
        zoey_df['Tags'] = pd.Series(netsuite_df.get('tags', ''))
        zoey_df['Published'] = pd.Series([True] * len(zoey_df))
        zoey_df['SKU'] = pd.Series(netsuite_df.get('variant sku', ''))
        zoey_df['Price'] = pd.Series(netsuite_df.get('variant price', 0.0)).fillna(0.0)  # Fill NaN values with 0.0
        zoey_df['Inventory Quantity'] = pd.Series(netsuite_df.get('inventory_qty', 0)).fillna(0)  # Ensure no NaN in inventory
        zoey_df['Barcode'] = pd.Series(netsuite_df.get('barcode', ''))
        zoey_df['Image URL'] = pd.Series(netsuite_df.get('image_url', ''))
        zoey_df['Image Alt Text'] = pd.Series(netsuite_df.get('image_alt_text', ''))

        logging.info(f"Mapping {len(zoey_df)} products from NetSuite to Zoey format completed successfully.")
        return zoey_df

    except KeyError as e:
        logging.error(f"KeyError during NetSuite to Zoey mapping: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    except Exception as err:
        logging.error(f"An unexpected error occurred during NetSuite to Zoey mapping: {err}")
        return pd.DataFrame()
