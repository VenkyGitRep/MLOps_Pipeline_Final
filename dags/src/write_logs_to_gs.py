import re
from google.cloud import storage
import os

def extract_full_manual_timestamp(dag_run_text):
    """
    Extracts the full manual timestamp from a formatted string, including the prefix 'manual__'.

    Args:
    text (str): The string containing the timestamp.

    Returns:
    str: The extracted full manual timestamp or None if no match is found.
    """
    # Define the regular expression pattern for the timestamp including 'manual__'
    # This captures the whole part from 'manual__' followed by the ISO 8601 date-time format
    pattern = r"(manual__\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[+-]\d{2}:\d{2})"
    print("Dag runtext:",dag_run_text)
    # Search for the pattern in the text
    match = re.search(pattern, str(dag_run_text))

    if match:
        # Return the matching group which contains the full manual timestamp
        return match.group(1)
    else:
        # Return None if no match is found
        return None

def write_to_gcs(**kwargs):
    """
    Recursively uploads all files from a directory to Google Cloud Storage.

    Args:
    kwargs: Dict containing context variables from Airflow.

    Assumes 'dag_run' key in kwargs can be used to extract a timestamp or identifier.
    """
    print("kwargs:",kwargs)
    print("Logs file:",extract_full_manual_timestamp(kwargs['dag_run']))
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
    bucket_name = 'dvc_bucket_mlops_lab'
    source_dir = os.path.join(BASE_DIR,'logs/dag_id=MLOP_pro/run_id=' + extract_full_manual_timestamp(kwargs['dag_run']))
    destination_dir = 'airflowlogs/'+extract_full_manual_timestamp(kwargs['dag_run'])
    credentials_path = 'dags/gs_connection/pelagic-bastion-421018-e735856b7b30.json'

    # Create a storage client using the credentials file
    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)
    
    # Walk through the source directory, and upload each file
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Construct the full GCS path where the file will be stored
            relative_path = os.path.relpath(file_path, source_dir)
            blob_path = os.path.join(destination_dir, relative_path)
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(file_path)
            print(f"Uploaded {file_path} to {blob_path}.")


# Example usage

#upload_to_gcs(bucket_name, source_file_path, destination_path, credentials_path)
