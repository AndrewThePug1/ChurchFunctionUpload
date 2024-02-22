import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Parse the incoming JSON
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # Convert the JSON data to a string to save it in a blob
    data = json.dumps(req_body)

    # Use an environment variable to store your connection string
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "songs-scc"

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Generate a blob name
    blob_name = f"songmetadata-{req_body['metadata']['title'].replace(' ', '-')}.json"

    # Upload the JSON data to the blob
    try:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        return func.HttpResponse(f"File successfully uploaded to {blob_name}.", status_code=200)
    except Exception as e:
        logging.error(f"Error uploading blob: {str(e)}")
        return func.HttpResponse("Failed to upload file to blob storage.", status_code=500)
