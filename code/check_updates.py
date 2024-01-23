import os
import requests
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()
project_id = os.environ.get("PROJECT_ID")
with open("secrets.json", "r") as source:
    info = json.load(source)
storage_credentials = service_account.Credentials.from_service_account_info(info)


def download_blob(bucket_name, source_blob_name):
    storage_client = storage.Client(project=project_id, credentials=storage_credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    file = blob.download_as_text()
    return file


def upload_blob(bucket_name, source_file, destination_blob_name):
    storage_client = storage.Client(project=project_id, credentials=storage_credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file)


def check_latest_commit(url):
    latest_commit_hash = requests.get(url).json()[0]["sha"]
    previous_hash = download_blob(bucket_name="blood-donation-github", source_blob_name="github-hash.txt")
    if previous_hash != latest_commit_hash:
        upload_blob(bucket_name="blood-donation-github", source_file=StringIO(latest_commit_hash).read(), destination_blob_name="github-hash.txt")
        return True
    else:
        return False


if __name__ == "__main__":
    pass