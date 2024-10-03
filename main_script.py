import argparse
import logging
from orchestrator.data_orchestrator import sync_netsuite_to_shopify, sync_netsuite_to_zoey, sync_shopify_to_zoey
from data_mapping.zoey_mapping import generate_mock_zoey_csv, fetch_data_from_zoey

def main(platform):
    """
    Main function to handle data synchronization or mock data generation based on the provided platform.

    Parameters:
        platform (str): The target platform for product data export or mock generation. Options are:
                        'netsuite_to_shopify', 'netsuite_to_zoey', 'shopify_to_zoey', 'generate_mock_zoey', 'fetch_from_zoey'
    """
    try:
        if platform == 'netsuite_to_shopify':
            logging.info("Starting synchronization from NetSuite to Shopify...")
            sync_netsuite_to_shopify()
        elif platform == 'netsuite_to_zoey':
            logging.info("Starting synchronization from NetSuite to Zoey...")
            sync_netsuite_to_zoey()
        elif platform == 'shopify_to_zoey':
            logging.info("Starting synchronization from Shopify to Zoey...")
            sync_shopify_to_zoey()
        elif platform == 'generate_mock_zoey':
            logging.info("Generating mock CSV data for Zoey import...")
            generate_mock_zoey_csv()
        elif platform == 'fetch_from_zoey':
            logging.info("Fetching data directly from Zoey via API...")
            zoey_data = fetch_data_from_zoey()
            
            # If data is fetched successfully, export to CSV
            if not zoey_data.empty:
                output_file = 'zoey_exported_data.csv'
                zoey_data.to_csv(output_file, index=False)
                logging.info(f"Zoey product data exported successfully to {output_file}")
            else:
                logging.warning("No data fetched from Zoey or data is empty.")
        else:
            logging.error(f"Unsupported platform: {platform}. Please choose from 'netsuite_to_shopify', 'netsuite_to_zoey', 'shopify_to_zoey', 'generate_mock_zoey', or 'fetch_from_zoey'.")
            return

        logging.info(f"Operation for {platform} completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the operation: {e}")
        raise  # Re-raise the exception for visibility or future handling if needed

if __name__ == "__main__":
    # Configure logging to display the timestamp and log level for each message
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set up argument parser for the platform input
    parser = argparse.ArgumentParser(description='Data synchronization tool for multiple platforms.')
    parser.add_argument('--platform', type=str, required=True,
                        help="Target platform for product data export. Options are: 'netsuite_to_shopify', 'netsuite_to_zoey', 'shopify_to_zoey', 'generate_mock_zoey', 'fetch_from_zoey'.")
    
    # Parse the provided arguments
    args = parser.parse_args()
    
    # Execute the main function with the provided platform argument
    main(args.platform)
