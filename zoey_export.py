# zoey_export.py

import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def export_to_zoey(df):
    """
    Exports product data to Zoey via its REST API.

    Parameters:
        df (pandas.DataFrame): DataFrame containing product information.

    Returns:
        bool: True if export is successful, False otherwise.
    """
    try:
        # Zoey API endpoint for products (replace with actual endpoint)
        api_url = "https://api.zoey.com/v1/products"

        # Retrieve API key from environment variables
        api_key = os.getenv('ZOEY_API_KEY')

        # Check if API key is available
        if not api_key:
            logging.error("Zoey API key not found. Please set the ZOEY_API_KEY environment variable.")
            return False

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        for index, row in df.iterrows():
            product_data = {
                "handle": row['Handle'],
                "title": row['Title'],
                "description": row['Body (HTML)'],
                "vendor": row['Vendor'],
                "type": row['Type'],
                "tags": row['Tags'],
                "published": row['Published'],
                "variants": [
                    {
                        "sku": row['Variant SKU'],
                        "price": row['Variant Price'],
                        "inventory_quantity": row['Variant Inventory Qty'],
                        "barcode": row['Variant Barcode'],
                        # Add other variant-specific fields as needed
                    }
                ],
                "images": [
                    {
                        "src": row['Image Src'],
                        "alt_text": row['Image Alt Text']
                    }
                ],
                # Add other product-specific fields as needed
            }

            response = requests.post(api_url, headers=headers, json=product_data)

            if response.status_code in [200, 201]:
                logging.info(f"Product '{row['Title']}' exported successfully to Zoey.")
            else:
                logging.error(f"Failed to export product '{row['Title']}' to Zoey: {response.status_code} - {response.text}")
                return False

        return True

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while exporting to Zoey: {http_err}")
        return False
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred while exporting to Zoey: {conn_err}")
        return False
    except Exception as err:
        logging.error(f"An unexpected error occurred while exporting to Zoey: {err}")
        return False
