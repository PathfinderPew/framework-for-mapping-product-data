# data_mapping.py

import pandas as pd

def map_outputcsv_to_shopify(output_df):
    """
    Maps data to Shopify format and fills missing values appropriately.
    """
    # Clean the 'Body (HTML)' field if needed
    output_df['Body (HTML)'] = output_df['Body (HTML)'].apply(clean_html)
    
    # Fill missing values in object (string) columns with empty strings
    object_columns = output_df.select_dtypes(include='object').columns
    output_df[object_columns] = output_df[object_columns].fillna('')
    
    # Optionally, fill missing numeric values if desired
    # For example, fill numeric columns with zeros
    numeric_columns = output_df.select_dtypes(include=['float64', 'int64']).columns
    output_df[numeric_columns] = output_df[numeric_columns].fillna(0)
    
    # Ensure all necessary columns are present
    if 'Status' not in output_df.columns:
        output_df['Status'] = 'active'
    
    # Return the DataFrame
    return output_df

def clean_html(html_content):
    """
    Cleans HTML content by removing unwanted tags or attributes.
    For simplicity, this function currently strips leading and trailing whitespace.
    You can expand this function to perform more complex HTML cleaning if needed.
    """
    # Import the re module for regular expressions
    import re
    
    # Remove HTML tags using a regular expression
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
    
    return clean_text
