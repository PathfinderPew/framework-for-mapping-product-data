# main_script.py

from netsuite_fetch import fetch_netsuite_data
from data_mapping import map_outputcsv_to_shopify
from export_util import export_to_csv

def main():
    # Fetch and clean data from output.xlsx
    output_data = fetch_netsuite_data(file='output.xlsx')

    # Verify that data was fetched successfully
    if output_data.empty:
        print("No data fetched from output.xlsx.")
        return  # Exit if no data is available

    # Map the data to Shopify format
    shopify_data = map_outputcsv_to_shopify(output_data)

    # Export the data to a CSV file
    export_to_csv(shopify_data, filename='shopify_import.csv')
    print("Data export completed successfully.")

if __name__ == "__main__":
    main()
