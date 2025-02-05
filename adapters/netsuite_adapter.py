import pandas as pd
import logging
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from adapters.common_adapter import make_request  # Import shared request function

# Load environment variables
load_dotenv()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type(Exception))
def fetch_netsuite_products(api_url=None):
    """
    Fetches product information from NetSuite using REST API.
    
    Parameters:
        api_url (str): Optional parameter for specifying a different API endpoint. If not provided, will use default URL.
    
    Returns:
        pandas.DataFrame: DataFrame containing product data from NetSuite.
    """
    try:
        # Use default API URL if not provided
        if not api_url:
            api_url = "https://<ACCOUNT_ID>.suitetalk.api.netsuite.com/services/rest/record/v1/item"

        # Retrieve access token from environment variables
        access_token = os.getenv('NETSUITE_ACCESS_TOKEN')
        if not access_token:
            logging.error("NetSuite access token not found. Please set NETSUITE_ACCESS_TOKEN in .env.")
            return pd.DataFrame()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        params = {"limit": 1000, "offset": 0}
        all_products = []

        while True:
            # Make the request using shared `make_request` function
            response = make_request("GET", api_url, headers=headers, params=params)

            # Check for NoneType and error response handling
            if response is None:
                logging.error(f"Request to NetSuite failed: No response received for {api_url}.")
                return pd.DataFrame()

            # Check if the response status code is a success
            if response.status_code != 200:
                logging.error(f"Failed to fetch products from NetSuite. Status code: {response.status_code}, Response: {response.text}")
                return pd.DataFrame()  # Return empty DataFrame on failure

            # Parse JSON data from the response
            data = response.json()
            products = data.get('items', [])
            
            # If there are no products, break out of the loop (end of pagination)
            if not products:
                break

            # Append the fetched products to the overall list
            all_products.extend(products)
            params['offset'] += params['limit']  # Increment the offset for pagination

        # Convert the accumulated products into a DataFrame
        df = pd.DataFrame(all_products)
        logging.info(f"Fetched {len(df)} products from NetSuite via API.")
        return df

    except Exception as err:
        logging.error(f"An unexpected error occurred while fetching NetSuite products: {err}")
        return pd.DataFrame()


def fetch_netsuite_data_from_file(file='Test Shopify Sheet.xlsx'):
    """
    Reads NetSuite product data from an Excel file for offline testing.
    
    Parameters:
        file (str): Path to the Excel file containing the NetSuite data.
    
    Returns:
        pandas.DataFrame: DataFrame containing the cleaned and formatted product data.
    """
    try:
        # Read data from the Excel file
        output_df = pd.read_excel(file, engine='openpyxl')
        logging.info(f"Data successfully read from {file}")
        
        # Ensure 'Variant Price' is numeric
        output_df['Variant Price'] = pd.to_numeric(output_df['Variant Price'], errors='coerce')

        # Ensure key columns are of correct data types
        output_df['Variant SKU'] = output_df['Variant SKU'].astype(str)
        output_df['Title'] = output_df['Title'].astype(str)
        output_df['Body (HTML)'] = output_df['Body (HTML)'].astype(str)

        # Handle missing data by dropping rows without essential columns
        output_df.dropna(subset=['Variant SKU', 'Title'], inplace=True)
        
        # Fill missing values with default entries
        output_df['Variant Price'] = output_df['Variant Price'].fillna(0)
        output_df['Body (HTML)'] = output_df['Body (HTML)'].fillna('')

        # Reset index for the cleaned DataFrame
        output_df.reset_index(drop=True, inplace=True)

        logging.info(f"Data processed successfully from {file}.")
        return output_df

    except FileNotFoundError:
        logging.error(f"The file '{file}' was not found. Please check the file path and name.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"An error occurred while processing '{file}': {e}")
        return pd.DataFrame()
