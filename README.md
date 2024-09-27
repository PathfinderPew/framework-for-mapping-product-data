# product-data-mapping-framework
Python framework automates the process of preparing product data for import into Shopify. It reads product information from Excel (.xlsx) or CSV files, cleans and validates the data, maps it to Shopify's required CSV format, and generates an import-ready CSV file.


Data Extraction

Reads product data from Excel or CSV files.
Supports flexible input formats to accommodate various data sources.
Data Cleaning and Validation

Ensures all product fields are correctly formatted.
Handles missing or inconsistent data by filling defaults or excluding incomplete records.
Converts data types (e.g., prices to numeric values, descriptions to text).
Data Mapping

Maps source data fields to Shopify's required CSV format.
Customizable mapping functions to adapt to different data structures.
Includes mandatory and optional fields required by Shopify.
CSV Generation

Produces a shopify_import.csv file ready for import into Shopify.
Ensures correct encoding and handles special characters.
Getting Started
Install Dependencies

Make sure you have Python 3 installed. Install the required packages:

bash
Copy code
pip install -r requirements.txt
Add Your Product Data

Place your output.xlsx or output.csv file into the project directory.

Run the Script

Navigate to the project directory and run:

bash
Copy code
python main_script.py
Import to Shopify

Locate the generated shopify_import.csv file. In your Shopify admin panel:

Go to Products > All products.
Click Import.
Upload the shopify_import.csv file.
Follow the prompts to complete the import.
Project Structure
bash
Copy code
your-repo-name/
├── README.md
├── requirements.txt
├── main_script.py
├── netsuite_fetch.py
├── data_mapping.py
├── export_util.py
├── output.xlsx       # Your product data file
├── shopify_import.csv
└── .gitignore
Customization
Adjust Data Mapping

Modify data_mapping.py to change how your data fields are mapped to Shopify's CSV format.

Enhance Data Cleaning

Edit netsuite_fetch.py if you need additional data validation or cleaning steps.
