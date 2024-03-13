import os
import json
import pandas as pd
from google.cloud import storage
import pickle

# Get the current working directory
PROJECT_DIR = os.getcwd()
print(PROJECT_DIR)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(PROJECT_DIR, "key.json")

def load_data_from_gcp_and_save_as_pkl(pickle_path):
    try:
        # Define the destination directory for saving JSON files
        destination_dir = os.path.join(PROJECT_DIR, "data", "processed")

        # Copy specific files from GCP to the local directory
        files_to_copy = [
            "Data/train.json"
        ]

        # Create a client
        client = storage.Client()

        # Get the bucket
        bucket = client.get_bucket('pii_data_load')

        # List to store dictionaries (JSON contents)
        json_contents_list = []

        for file in files_to_copy:
            # Get the blob
            blob = storage.Blob(file, bucket)
            # Download the file to a destination
            blob.download_to_filename(os.path.join(destination_dir, os.path.basename(file)))
            # Read JSON file
            with open(os.path.join(destination_dir, os.path.basename(file)), 'r') as json_file:
                json_contents = json.load(json_file)
                json_contents_list.append(json_contents)

        # Save the list of JSON contents as a pickle file
        with open(pickle_path, 'wb') as f:
            pickle.dump(json_contents_list, f)

        print("Data loaded and saved as pkl successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Specify the path where you want to save the pickle file
pickle_path = os.path.join(PROJECT_DIR, "data", "processed", "data.pkl")
print(pickle_path)
# Call the function to load data from GCP and save it as pkl
load_data_from_gcp_and_save_as_pkl(pickle_path)