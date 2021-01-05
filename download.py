import os, os.path
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient

CONNECT_STR = ""
CONTAINER_NAME = "blobtest"

container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)

output_blob_name

print("Now Downloading blob...")
download_file_path = os.path.join("./vide", str.replace(output_blob_name ,'.avi', '_DOWNLOAD.avi'))
with open(download_file_path, "wb") as download_file:
    download_file.write(container_client.download_blob(output_blob_name).readall())

print("Press any key to delete file in the container")
input()
container_client.delete_blob(blob=output_blob_name)
print("Delete Complete. Exiting...")
