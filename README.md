Automated Data Transfer Framework

This Python framework makes it super easy to get your product data ready for e-commerce platforms like Shopify and Zoey. It takes care of reading data from Excel or CSV files, cleaning it up, mapping it to the right format, and then exporting it so you can import it right into your store.

What It Does
1. Data Extraction
Reads product data from Excel (.xlsx) and CSV files.
Can also pull data directly from APIs like NetSuite.
Supports flexible file formats so you don’t have to worry about changing your data structure.
2. Data Cleaning and Validation
Makes sure your data is formatted correctly.
Handles missing data by filling in defaults or dropping incomplete records.
Cleans up HTML descriptions, normalizes column names, and validates numeric fields.
3. Data Mapping
Converts your data to fit Shopify’s and Zoey’s formats.
Maps all the fields you need, like SKU, price, and descriptions.
You can customize the mapping rules to suit your own data needs.
4. Data Export
Creates ready-to-import files for Shopify or Zoey.
Supports multiple formats like CSV, Excel, and JSON.
Customizable export options for different platforms.
5. API Integration and Automation
Directly syncs with NetSuite, Shopify, and Zoey using their APIs.
Perfect for automating data updates or building a real-time integration.

Getting Started
1. Set Up
First, make sure you have Python 3.x installed, and then install all the required packages:

pip install -r requirements.txt

2. Configure Your Environment
Create a .env file in the root folder and add your API keys and configurations. For example:

NETSUITE_ACCESS_TOKEN=your_netsuite_access_token
ZOEY_API_KEY=your_zoey_api_key

3. Add Your Data
Place your output.xlsx or output.csv file into the project folder (automated_data_transfer_framework/).
Make sure your data matches the expected structure. Check out the data_mapping folder for details on what columns are required.

4. Run the Framework
Run the main script to start processing your data:


```bash
python main_script.py
```

5. Import to Shopify or Zoey
For Shopify:
Go to your Shopify admin panel: Products > All products.
Click Import and select the shopify_import.csv file that was created.
Follow the steps to finish the import.
For Zoey:
Configure the zoey_adapter.py to automatically push data using the Zoey API or use the exported CSV.

Customizing the Framework
Adjust Data Mapping
Want to change how your data is structured for Shopify or Zoey? Just update the relevant files in the data_mapping/ folder to change the field mapping and formatting rules.
Add Extra Data Cleaning
If you need more validation steps, check out the common_mapping.py file for shared cleaning functions like clean_html and normalize_column_names. You can tweak those or add new ones to meet your needs.
Automate with AWS Lambda
Deploy the framework to AWS Lambda for automatic updates. You can containerize it using Docker and set up a serverless deployment for real-time data syncing.

Running the Tests
Run all the tests to make sure everything’s working:



```bash
python -m unittest discover -v tests
```


Troubleshooting
Data isn’t mapping correctly? Double-check the column names in your source file.
API keys missing? Make sure your .env file has the right keys and they’re correctly loaded.
Check the logs for more details if something seems off!



