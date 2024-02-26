import os
from utils.azure_blob_handler import AzureBlobHandler
from dotenv import load_dotenv

load_dotenv()
SAVE_DIR = os.getenv('RESOURCE_PATH')


def download_resources(container_name):
    """ download resources """
    blob_handler = AzureBlobHandler()
    blob_list = blob_handler.get_blob_list(container_name)
    for blob in blob_list:
        print(f"Downloading blob file: {blob.name}")
        blob_handler.download_file(container_name, blob.name)


def validate_resources():
    """ validate resources """
    if not os.listdir(SAVE_DIR):
        return False
    return True
