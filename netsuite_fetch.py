# netsuite_fetch.py

import pandas as pd

def fetch_netsuite_data(file='Test Shopify Sheet.xlsx'):
    """
    Fetches product data from an Excel (.xlsx) file and ensures data compatibility.
    """
    try:
        # Step 1: Read data from the Excel file
        output_df = pd.read_excel(file, engine='openpyxl')
        print(f"Data successfully read from {file}")
        
        # Optional: Print column names for verification
        print("Columns in DataFrame:", output_df.columns.tolist())
        
        # Step 2: Ensure 'Variant Price' is numeric
        output_df['Variant Price'] = pd.to_numeric(output_df['Variant Price'], errors='coerce')
        
        # Step 3: Ensure key columns are of correct data types
        output_df['Variant SKU'] = output_df['Variant SKU'].astype(str)
        output_df['Title'] = output_df['Title'].astype(str)
        output_df['Body (HTML)'] = output_df['Body (HTML)'].astype(str)
        
        # Step 4: Handle missing data
        # Drop rows where 'Variant SKU' or 'Title' is missing
        output_df.dropna(subset=['Variant SKU', 'Title'], inplace=True)
        
        # Fill missing 'Variant Price' values with 0
        output_df['Variant Price'] = output_df['Variant Price'].fillna(0)
        
        # Fill missing 'Body (HTML)' with an empty string
        output_df['Body (HTML)'] = output_df['Body (HTML)'].fillna('')
        
        # Step 5: Reset the index after dropping rows
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
        print(f"An error occurred while processing {file}: {e}")
        return pd.DataFrame()
