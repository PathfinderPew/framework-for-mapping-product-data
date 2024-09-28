# main_script.py

import argparse
import logging
from netsuite_fetch import fetch_netsuite_products
from data_mapping import map_outputcsv_to_shopify, map_output_to_zoey
from export_util import export_to_csv
from zoey_export import export_to_zoey
# If you have a Shopify fetch module, import it as well

def main(platform):
    if platform == 'shopify':
        # Fetch and clean data from Shopify Excel file
        output_data = fetch_shopify_data(file='Test Shopify Sheet.xlsx')  # Ensure this function exists
        # Map to Shopify format
        mapped_data = map_outputcsv_to_shopify(output_data)
        # Export to Shopify CSV
        export_to_csv(mapped_data, filename='shopify_import.csv')
    elif platform == 'netsuite':
        # Fetch and clean data from NetSuite
        output_data = fetch_netsuite_products()
        # Map to Zoey format
        mapped_data = map_output_to_zoey(output_data)
        # Export via Zoey API
        success = export_to_zoey(mapped_data)
        if not success:
            logging.error("Failed to export data to Zoey via API.")
    elif platform == 'zoey_csv':
        # Fetch data from NetSuite or Shopify as needed
        output_data = fetch_netsuite_products()  # Or fetch_shopify_data()
        # Map to Zoey CSV format
        mapped_data = map_output_to_zoey(output_data)
        # Export to Zoey CSV
        export_to_csv(mapped_data, filename='zoey_import.csv')
    else:
        print(f"Unsupported platform: {platform}")
        return

    print("Data export completed successfully.")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Export product data to various platforms.')
    parser.add_argument('--platform', type=str, required=True,
                        help='Target platform for product data export (shopify/netsuite/zoey_csv)')
    args = parser.parse_args()
    main(args.platform)
