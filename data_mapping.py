# data_mapping.py

import pandas as pd
import re
import logging

def map_output_to_zoey(df):
    """
    Maps data from NetSuite or Shopify to Zoey's required format.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing product information.
        
    Returns:
        pandas.DataFrame: Mapped DataFrame ready for Zoey's import.
    """
    # Clean the 'Body (HTML)' field
    df['Body (HTML)'] = df['Body (HTML)'].apply(clean_html)
    
    # Fill missing values appropriately based on data types
    object_columns = df.select_dtypes(include='object').columns
    df[object_columns] = df[object_columns].fillna('')
    
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Ensure all necessary columns are present
    if 'Status' not in df.columns:
        df['Status'] = 'active'
    
    # Example: Map columns to Zoey's expected format
    zoey_df = pd.DataFrame()
    zoey_df['Handle'] = df['Handle']
    zoey_df['Title'] = df['Title']
    zoey_df['Description'] = df['Body (HTML)']
    zoey_df['Vendor'] = df['Vendor']
    zoey_df['Type'] = df['Type']
    zoey_df['Tags'] = df['Tags']
    zoey_df['Published'] = df['Published']
    zoey_df['SKU'] = df['Variant SKU']
    zoey_df['Price'] = df['Variant Price']
    zoey_df['Inventory Quantity'] = df['Variant Inventory Qty']
    zoey_df['Barcode'] = df['Variant Barcode']
    zoey_df['Image URL'] = df['Image Src']
    zoey_df['Image Alt Text'] = df['Image Alt Text']
    # Add other necessary mappings based on Zoey's requirements
    
    # Create 'Handle' from 'Title' if not already present
    zoey_df['Handle'] = zoey_df['Title'].str.lower().str.replace(' ', '-').str.replace('/', '-')
    
    # Ensure data types are correct
    zoey_df['Published'] = zoey_df['Published'].astype(bool)
    zoey_df['Price'] = zoey_df['Price'].astype(float)
    zoey_df['Inventory Quantity'] = zoey_df['Inventory Quantity'].astype(int)
    
    # Log mapping completion
    logging.info("Data mapping to Zoey's format completed.")
    
    return zoey_df

def clean_html(html_content):
    """
    Cleans HTML content by removing HTML tags and stripping whitespace.
    """
    # Remove HTML tags using regular expressions
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
    
    return clean_text

def map_outputcsv_to_shopify(df):
    """
    Maps data from Shopify or NetSuite to Shopify CSV format.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing product information.
        
    Returns:
        pandas.DataFrame: Mapped DataFrame ready for Shopify's import.
    """
    # Existing mapping logic for Shopify
    # Similar to map_output_to_zoey but tailored for Shopify
    pass  # Implement as per your existing logic
