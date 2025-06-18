from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# Replace with your actual values
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SITE_ID = "ea00a390-1e32-4dfa-aa56-04df02bf0191"
LIST_ID = "7149c67a-094e-4f89-a502-d5bbbfebce2b"

# Base URL for Microsoft Graph API
BASE_URL = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{LIST_ID}/items"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

def fetch_all_items_with_fields():
    url = BASE_URL
    all_items = []

    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        for item in data.get("value", []):
            item_id = item["id"]
            fields_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{LIST_ID}/items/{item_id}/fields"
            fields_response = requests.get(fields_url, headers=HEADERS)
            fields_response.raise_for_status()
            fields_data = fields_response.json()
            all_items.append({
                "id": item_id,
                "fields": fields_data
            })

        url = data.get("@odata.nextLink")

    return all_items

@app.get("/sharepoint-data-list")
def get_sharepoint_data():
    try:
        data = fetch_all_items_with_fields()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
