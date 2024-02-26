#!/usr/bin/env python3

"""
This is a module that Azure Blob Storage Connection.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


load_dotenv()
SAVE_DIR = os.getenv('RESOURCE_PATH')


class AzureBlobHandler:
    """ Azure Blob File Loader """
    def __init__(self):
        connection_string = os.getenv('AZURE_CONNECTION_STRING')
        self.blob_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.make_save_dir()

    @staticmethod
    def make_save_dir(dir_path=SAVE_DIR):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def create_container(self, container_name):
        """ create container """
        container_list = self.blob_client.list_containers(
            name_starts_with=container_name
        )
        container_exists = any(
            container.name == container_name for container in container_list
        )

        if not container_exists:
            self.blob_client.create_container(container_name)
            print(f"Container '{container_name}' created.")
        else:
            print(f"Container '{container_name}' already exists.")

    def upload_file(self, file_path, container_name, blob_name):
        """ upload file """
        container_name = "container-"+container_name
        # 컨테이너가 없으면 생성
        self.create_container(container_name)
        blob_client = self.blob_client.get_blob_client(
            container_name, blob_name
        )
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def download_files(self, file_path, container_name, blob_name):
        """ load file """
        container_name = "container-"+container_name
        container_client = self.get_container_client
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            print(f"Downloading blob file: {blob.name}")
            blob_client = self.blob_client.get_blob_client(
                container_name, blob.name
            )
            with open(os.path.join(SAVE_DIR, blob.name), "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

    def get_container_client(self, container_name):
        container_name = "container-"+str(container_name)
        container_client = self.blob_client.get_container_client(
            container_name
        )
        return container_client

    def get_blob_list(self, container_name):
        container_client = self.get_container_client(container_name)
        blob_list = container_client.list_blobs()

        return blob_list

    def download_file(self, container_name, blob_name):
        """ load file """
        container_name = "container-"+str(container_name)
        blob_client = self.blob_client.get_blob_client(
            container_name, blob_name
        )
        with open(os.path.join(SAVE_DIR, blob_name), "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
