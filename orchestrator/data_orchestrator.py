# orchestrator/data_orchestrator.py

import logging
from adapters import shopify_adapter, netsuite_adapter, zoey_adapter
from data_mapping import shopify_mapping, netsuite_mapping, zoey_mapping

# Configure logging to capture debug and info messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def sync_netsuite_to_shopify():
    """
    Synchronizes product data from NetSuite to Shopify.
    """
    logging.info("Starting NetSuite to Shopify synchronization...")

    # Step 1: Fetch data from NetSuite
    netsuite_data = netsuite_adapter.fetch_netsuite_products()
    if netsuite_data.empty:
        logging.warning("No data fetched from NetSuite. Synchronization aborted.")
        return

    # Step 2: Map NetSuite data to Shopify format
    shopify_ready_data = netsuite_mapping.map_to_shopify(netsuite_data)
    if shopify_ready_data.empty:
        logging.warning("Mapping to Shopify format failed. No data to upload.")
        return

    # Step 3: Upload mapped data to Shopify
    success = shopify_adapter.upload_products(shopify_ready_data)
    if success:
        logging.info("Data successfully synchronized from NetSuite to Shopify.")
    else:
        logging.error("Data upload to Shopify failed.")


def sync_netsuite_to_zoey():
    """
    Synchronizes product data from NetSuite to Zoey.
    """
    logging.info("Starting NetSuite to Zoey synchronization...")

    # Step 1: Fetch data from NetSuite
    netsuite_data = netsuite_adapter.fetch_netsuite_products()
    if netsuite_data.empty:
        logging.warning("No data fetched from NetSuite. Synchronization aborted.")
        return

    # Step 2: Map NetSuite data to Zoey format
    zoey_ready_data = netsuite_mapping.map_to_zoey(netsuite_data)
    if zoey_ready_data.empty:
        logging.warning("Mapping to Zoey format failed. No data to export.")
        return

    # Step 3: Export mapped data to Zoey
    success = zoey_adapter.export_to_zoey(zoey_ready_data)
    if success:
        logging.info("Data successfully synchronized from NetSuite to Zoey.")
    else:
        logging.error("Data export to Zoey failed.")


def sync_shopify_to_zoey():
    """
    Synchronizes product data from Shopify to Zoey.
    """
    logging.info("Starting Shopify to Zoey synchronization...")

    # Step 1: Fetch data from Shopify
    shopify_data = shopify_adapter.fetch_shopify_data(file='Test Shopify Sheet.xlsx')
    if shopify_data.empty:
        logging.warning("No data fetched from Shopify. Synchronization aborted.")
        return

    # Step 2: Map Shopify data to Zoey format
    zoey_ready_data = shopify_mapping.map_to_zoey(shopify_data)
    if zoey_ready_data.empty:
        logging.warning("Mapping to Zoey format failed. No data to export.")
        return

    # Step 3: Export mapped data to Zoey
    success = zoey_adapter.export_to_zoey(zoey_ready_data)
    if success:
        logging.info("Data successfully synchronized from Shopify to Zoey.")
    else:
        logging.error("Data export to Zoey failed.")
