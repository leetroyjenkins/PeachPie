#!/usr/bin/env python3

# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here
    account_url = "https://pastrychefazurestorage.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Check for existing container names
    container_list = [i for i in blob_service_client.list_containers()]

    # Check if <testcontainer> exists

    # Check for files in the test_results dir

    # Check if the files exist in the container

    # Upload any files that do not exist to the container

    # Delete the files from local

    # Create a unique name for the container
    container_name = str(uuid.uuid4())

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    # Create a local directory to hold blob data
    local_path = "./data"
    if not os.path.exists(local_path):
        os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write("Hello, World!")
    file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    
    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
    container_client = blob_service_client.get_container_client(container= container_name) 
    print("\nDownloading blob to \n\t" + download_file_path)
    
    with open(file=download_file_path, mode="wb") as download_file:
        #download_file.write(container_client.download_blob(blob.name).readall())
        download_file.write(container_client.download_blob(blob_client.blob_name).readall())

    # Clean up
    print("\nPress the Enter key to begin clean up")
    input()

    print("Deleting blob container...")
    container_client.delete_container()

    print("Deleting the local source and downloaded files...")
    os.remove(upload_file_path)
    os.remove(download_file_path)
    os.rmdir(local_path)

    print("Done")

except Exception as ex:
    print('Exception:')
    print(ex)