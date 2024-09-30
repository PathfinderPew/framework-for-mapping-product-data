# adapters/zoey_adapter.py

import pandas as pd
import logging
import os
from dotenv import load_dotenv
from adapters.common_adapter import make_request  # Import shared request function

# Load environment variables
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
        # Replace with Zoey's actual API endpoint for product creation
        api_url = "https://api.zoey.com/v1/products"

        # Retrieve API key from environment variables
        api_key = os.getenv('ZOEY_API_KEY')
        if not api_key:
            logging.error("Zoey API key not found. Please set ZOEY_API_KEY in .env.")
            return False

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Iterate through the rows in the DataFrame and export each product to Zoey
        for _, row in df.iterrows():
            product_data = {
                "handle": row.get('Handle', ''),
                "title": row.get('Title', ''),
                "description": row.get('Description', ''),
                "vendor": row.get('Vendor', ''),
                "type": row.get('Type', ''),
                "tags": row.get('Tags', ''),
                "published": row.get('Published', False),
                "variants": [
                    {
                        "sku": row.get('SKU', ''),
                        "price": row.get('Price', 0.0),
                        "inventory_quantity": row.get('Inventory Quantity', 0),
                        "barcode": row.get('Barcode', '')
                    }
                ],
                "images": [
                    {
                        "src": row.get('Image URL', ''),
                        "alt_text": row.get('Image Alt Text', '')
                    }
                ]
            }

            # Use shared `make_request` function to handle the HTTP POST request
            response = make_request("POST", api_url, headers=headers, data=product_data)

            # Check if response is None before attempting to access its attributes
            if response is None:
                logging.error(f"Request failed for product '{row.get('Title', 'N/A')}'.")
                return False

            # Check the response status code and log the result
            if response.status_code in [200, 201]:
                logging.info(f"Product '{row.get('Title', 'N/A')}' exported successfully to Zoey.")
            else:
                logging.error(f"Failed to export product '{row.get('Title', 'N/A')}' to Zoey: {response.status_code} - {response.text}")
                return False  # Optionally, you can choose to continue exporting other products

        return True

    except Exception as err:
        logging.error(f"An unexpected error occurred while exporting to Zoey: {err}")
        return False
