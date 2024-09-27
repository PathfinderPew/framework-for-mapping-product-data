# data_mapping.py

import pandas as pd

def map_outputcsv_to_shopify(output_df):
    """
    Maps data from output.csv to Shopify CSV format.
    """
    # Define Shopify columns
    shopify_columns = [
        'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published',
        'Option1 Name', 'Option1 Value', 'Variant SKU', 'Variant Grams',
        'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
        'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
        'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode',
        'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card',
        'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category',
        'Google Shopping / Gender', 'Google Shopping / Age Group',
        'Google Shopping / MPN', 'Google Shopping / AdWords Grouping',
        'Google Shopping / AdWords Labels', 'Google Shopping / Condition',
        'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0',
        'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
        'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4',
        'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item',
        'Status'
    ]

    # Initialize the Shopify DataFrame
    shopify_df = pd.DataFrame(columns=shopify_columns)

    # Map data
    shopify_df['Handle'] = output_df['name'].str.lower().str.replace(' ', '-').str.replace('/', '-')
    shopify_df['Title'] = output_df['name']
    shopify_df['Body (HTML)'] = output_df['description']
    shopify_df['Vendor'] = output_df['brand']  # Map 'brand' to 'Vendor'
    shopify_df['Type'] = 'Fire Safety Equipment'  # Adjust as necessary
    shopify_df['Tags'] = ''  # Add tags if available
    shopify_df['Published'] = 'TRUE'
    shopify_df['Option1 Name'] = 'Title'
    shopify_df['Option1 Value'] = 'Default Title'
    shopify_df['Variant SKU'] = output_df['sku']
    shopify_df['Variant Inventory Tracker'] = ''  # 'shopify', 'amazon', etc., if applicable
    shopify_df['Variant Inventory Qty'] = ''  # Add inventory quantity if available
    shopify_df['Variant Inventory Policy'] = 'deny'  # Options: 'deny' or 'continue'
    shopify_df['Variant Fulfillment Service'] = 'manual'
    shopify_df['Variant Price'] = output_df['price']
    shopify_df['Variant Compare At Price'] = ''  # Original price if on sale
    shopify_df['Variant Requires Shipping'] = 'TRUE'
    shopify_df['Variant Taxable'] = 'TRUE'
    shopify_df['Variant Barcode'] = ''  # If you have barcode data
    shopify_df['Image Src'] = output_df['image_url']
    shopify_df['Image Position'] = 1
    shopify_df['Image Alt Text'] = shopify_df['Title']
    shopify_df['Gift Card'] = 'FALSE'
    shopify_df['SEO Title'] = shopify_df['Title']
    shopify_df['SEO Description'] = shopify_df['Body (HTML)'].str.slice(0, 320)
    shopify_df['Google Shopping / Google Product Category'] = ''
    shopify_df['Google Shopping / Gender'] = ''
    shopify_df['Google Shopping / Age Group'] = ''
    shopify_df['Google Shopping / MPN'] = ''
    shopify_df['Google Shopping / AdWords Grouping'] = ''
    shopify_df['Google Shopping / AdWords Labels'] = ''
    shopify_df['Google Shopping / Condition'] = 'New'
    shopify_df['Google Shopping / Custom Product'] = ''
    shopify_df['Google Shopping / Custom Label 0'] = ''
    shopify_df['Google Shopping / Custom Label 1'] = ''
    shopify_df['Google Shopping / Custom Label 2'] = ''
    shopify_df['Google Shopping / Custom Label 3'] = ''
    shopify_df['Google Shopping / Custom Label 4'] = ''
    shopify_df['Variant Image'] = ''
    shopify_df['Variant Weight Unit'] = 'lb'  # Adjust if necessary
    shopify_df['Variant Tax Code'] = ''
    shopify_df['Cost per item'] = ''  # If you have cost data
    shopify_df['Status'] = 'active'  # Options: 'active', 'draft', or 'archived'

    # Replace NaN with empty strings
    shopify_df.fillna('', inplace=True)

    return shopify_df
