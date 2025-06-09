from fastapi import FastAPI
import os
import requests

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SITE_ID = "ea00a390-1e32-4dfa-aa56-04df02bf0191"

app = FastAPI()

def fetch_lists(token):
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

def fetch_list_items(token, list_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{list_id}/items?expand=fields"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

@app.get("/sharepoint-data")
def fetch_data():
    lists = fetch_lists(ACCESS_TOKEN)
    all_data = {}
    for list_item in lists:
        list_id = list_item["id"]
        list_name = list_item["displayName"]
        items = fetch_list_items(ACCESS_TOKEN, list_id)
        all_data[list_name] = items
    return {"lists": all_data}
