import requests
from .config import API_UPLOAD, API_HISTORY, API_DOWNLOAD, AUTH_CREDENTIALS

def fetch_history():
    return requests.get(API_HISTORY, auth=AUTH_CREDENTIALS)

def upload_csv(file_path):
    with open(file_path, "rb") as f:
        return requests.post(API_UPLOAD, files={"file": f}, auth=AUTH_CREDENTIALS)

def download_pdf(dataset_id):
    url = f"{API_DOWNLOAD}?id={dataset_id}"
    return requests.get(url, auth=AUTH_CREDENTIALS)
