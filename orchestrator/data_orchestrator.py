# orchestrator/data_orchestrator.py

from adapters import shopify_adapter, netsuite_adapter, zoey_adapter
from data_mapping import shopify_mapping, netsuite_mapping, zoey_mapping

def sync_netsuite_to_shopify():
    # Step 1: Fetch data from NetSuite
    netsuite_data = netsuite_adapter.fetch_netsuite_products()
    
    # Step 2: Map to Shopify format
    shopify_ready_data = netsuite_mapping.map_to_shopify(netsuite_data)
    
    # Step 3: Upload to Shopify
    shopify_adapter.upload_products(shopify_ready_data)

def sync_netsuite_to_zoey():
    # Step 1: Fetch data from NetSuite
    netsuite_data = netsuite_adapter.fetch_netsuite_products()
    
    # Step 2: Map to Zoey format
    zoey_ready_data = netsuite_mapping.map_to_zoey(netsuite_data)
    
    # Step 3: Export to Zoey
    zoey_adapter.export_to_zoey(zoey_ready_data)

def sync_shopify_to_zoey():
    # Step 1: Fetch data from Shopify
    shopify_data = shopify_adapter.fetch_shopify_data(file='Test Shopify Sheet.xlsx')
    
    # Step 2: Map to Zoey format
    zoey_ready_data = shopify_mapping.map_to_zoey(shopify_data)
    
    # Step 3: Export to Zoey
    zoey_adapter.export_to_zoey(zoey_ready_data)
