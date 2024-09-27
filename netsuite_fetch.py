# netsuite_fetch.py

import pandas as pd

def fetch_netsuite_data(file='output.xlsx'):
    """
    Fetches product data from an Excel (.xlsx) file and ensures data compatibility.
    """
    try:
        # Step 1: Read data from the Excel file
        output_df = pd.read_excel(file, engine='openpyxl')
        print(f"Data successfully read from {file}")
        
        # Step 2: Convert column names to lowercase
        output_df.columns = output_df.columns.str.lower()
        
        # Step 3: Ensure 'price' is numeric
        output_df['price'] = pd.to_numeric(output_df['price'], errors='coerce')
        
        # Step 4: Ensure 'sku', 'name', and 'description' are strings
        output_df['sku'] = output_df['sku'].astype(str)
        output_df['name'] = output_df['name'].astype(str)
        output_df['description'] = output_df['description'].astype(str)
        
        # Step 5: Handle missing data
        # Drop rows where 'sku' or 'name' is missing
        output_df.dropna(subset=['sku', 'name'], inplace=True)
        
        # Fill missing 'price' values with 0
        output_df['price'] = output_df['price'].fillna(0)
        
        # Fill missing 'description' with an empty string
        output_df['description'] = output_df['description'].fillna('')
        
        # Step 6: Reset the index after dropping rows
        output_df.reset_index(drop=True, inplace=True)
        
        # Optional: Print data types and a preview for verification
        print("Data types after processing:\n", output_df.dtypes)
        print("First few rows of processed data:\n", output_df.head())
        
        # Return the cleaned DataFrame
        return output_df

    except FileNotFoundError:
        print(f"The file {file} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while reading {file}: {e}")
        return pd.DataFrame()
