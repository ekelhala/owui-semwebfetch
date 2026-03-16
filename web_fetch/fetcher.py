import os
import requests

# The Browserless URL can be overridden via an env var.
# Default is the same as before.
API_URL = os.getenv("BROWSERLESS_API_URL", "http://browserless:3000/content")

def fetch_page(url: str) -> str:
    """
    Use Browserless to fetch a page and return the raw HTML string.
    """
    payload = {
        "url": url,
        "gotoOptions": {"waitUntil": "networkidle2", "timeout": 30000},
    }
    r = requests.post(API_URL, json=payload, timeout=45)
    r.raise_for_status()
    return r.text