# main_script.py

import argparse
import logging
from orchestrator.data_orchestrator import sync_netsuite_to_shopify, sync_netsuite_to_zoey, sync_shopify_to_zoey

def main(platform):
    if platform == 'shopify':
        logging.info("Starting synchronization from NetSuite to Shopify...")
        sync_netsuite_to_shopify()
    elif platform == 'netsuite_zoey':
        logging.info("Starting synchronization from NetSuite to Zoey...")
        sync_netsuite_to_zoey()
    elif platform == 'shopify_zoey':
        logging.info("Starting synchronization from Shopify to Zoey...")
        sync_shopify_to_zoey()
    else:
        logging.error(f"Unsupported platform: {platform}")
        return

    logging.info("Data synchronization completed successfully.")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Data synchronization for multiple platforms.')
    parser.add_argument('--platform', type=str, required=True,
                        help='Target platform for product data export (shopify/netsuite_zoey/shopify_zoey)')
    args = parser.parse_args()
    main(args.platform)
