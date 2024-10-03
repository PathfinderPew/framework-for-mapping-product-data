import pandas as pd
import re
import logging

def clean_html(html_content):
    """
    Cleans HTML content by removing HTML tags and stripping whitespace.

    Parameters:
        html_content (str): HTML content to clean.

    Returns:
        str: Cleaned text without HTML tags.
    """
    if not html_content:
        return ""
    # Remove HTML tags using regular expressions
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    
    # Remove leading and trailing whitespace
    clean_text = clean_text.strip()
    
    return clean_text

def normalize_column_names(df):
    """
    Normalizes the column names of a DataFrame by converting them to lowercase,
    replacing spaces with underscores, and removing special characters.
    
    Parameters:
        df (pandas.DataFrame): Input DataFrame with columns to normalize.
    
    Returns:
        pandas.DataFrame: DataFrame with normalized column names.
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('[()]', '', regex=True)
    )
    logging.info(f"Normalized columns: {df.columns.tolist()}")
    return df

def fill_missing_values(df):
    """
    Fills missing values in a DataFrame based on the column data types.
    
    Parameters:
        df (pandas.DataFrame): Input DataFrame with missing values.
    
    Returns:
        pandas.DataFrame: DataFrame with filled values.
    """
    try:
        # Isolate columns based on data type
        object_columns = df.select_dtypes(include='object').columns
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

        # Fill missing values for object columns with empty strings, using .loc to avoid misalignment
        for col in object_columns:
            if col in df.columns:
                df.loc[:, col] = df[col].fillna('')
        
        # Fill missing values for numeric columns with 0, using .loc to ensure alignment
        for col in numeric_columns:
            if col in df.columns:
                df.loc[:, col] = df[col].fillna(0)

        logging.info(f"Missing values filled. DataFrame shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"An error occurred while filling missing values: {e}")
        raise
