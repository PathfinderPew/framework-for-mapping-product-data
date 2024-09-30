# adapters/common_adapter.py

import requests
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Custom exception classes for more granular error handling
class APIConnectionError(Exception):
    pass

class APITimeoutError(Exception):
    pass

# Generic retry configuration
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)))
def make_request(method, url, headers=None, params=None, data=None):
    """
    Makes a generic HTTP request with retries and error handling.
    
    Parameters:
        method (str): HTTP method ('GET', 'POST', etc.)
        url (str): API endpoint URL.
        headers (dict): HTTP headers.
        params (dict): Query parameters.
        data (dict): Request body for POST/PUT requests.
    
    Returns:
        response: The full HTTP response object.
    """
    try:
        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response  # Return the full response object
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        raise APIConnectionError("Failed to establish a new connection.")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
        raise APITimeoutError("Request timed out.")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
        raise
