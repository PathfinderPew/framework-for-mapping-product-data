# export_util.py

def export_to_csv(shopify_df, filename='shopify_import.csv'):
    """
    Exports the Shopify DataFrame to a CSV file.
    """
    shopify_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Data exported to {filename}")
