# convert_product.py

import os
import sys
import pandas as pd
from data_mapping import map_to_shopify, map_netsuite_to_zoey, map_shopify_to_zoey
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_product(source_format, destination_format, source_file_path, output_file_path):
    """
    Converts product data from one format to another and saves it as a new file.

    Parameters:
        source_format (str): The source format (e.g., 'shopify', 'netsuite').
        destination_format (str): The destination format (e.g., 'shopify', 'zoey', 'netsuite').
        source_file_path (str): Path to the input file.
        output_file_path (str): Path to save the converted file.
    """
    try:
        # Load the source file
        logging.info(f"Loading source file: {source_file_path}")
        source_df = pd.read_excel(source_file_path)

        # Select the appropriate mapping function based on the formats
        if source_format == 'shopify' and destination_format == 'netsuite':
            mapped_df = map_to_shopify(source_df)
        elif source_format == 'netsuite' and destination_format == 'zoey':
            mapped_df = map_netsuite_to_zoey(source_df)
        elif source_format == 'shopify' and destination_format == 'zoey':
            mapped_df = map_shopify_to_zoey(source_df)
        else:
            logging.error(f"Unsupported conversion: {source_format} to {destination_format}")
            return

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the mapped DataFrame to the output file path
        logging.info(f"Saving converted file to: {output_file_path}")
        mapped_df.to_excel(output_file_path, index=False)

        logging.info(f"Conversion from {source_format} to {destination_format} completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred during the conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure that the command-line arguments are correct
    if len(sys.argv) != 5:
        logging.error("Usage: python convert_product.py <source_format> <destination_format> <source_file_path> <output_file_path>")
        sys.exit(1)

    # Parse command-line arguments
    source_format = sys.argv[1]
    destination_format = sys.argv[2]
    source_file_path = sys.argv[3]
    output_file_path = sys.argv[4]

    # Execute the conversion
    convert_product(source_format, destination_format, source_file_path, output_file_path)
