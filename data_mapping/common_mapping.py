# common_mapping.py

import pandas as pd
import re

def clean_html(html_content):
    """
    Cleans HTML content by removing HTML tags and stripping whitespace.
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
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[()]', '', regex=True)
    return df

def fill_missing_values(df):
    """
    Fills missing values in a DataFrame based on the column data types.
    
    Parameters:
        df (pandas.DataFrame): Input DataFrame with missing values.
    
    Returns:
        pandas.DataFrame: DataFrame with filled values.
    """
    object_columns = df.select_dtypes(include='object').columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    
    df[object_columns] = df[object_columns].fillna('')
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    return df
