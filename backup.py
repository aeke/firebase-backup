# -*- coding: utf-8 -*-
import uuid
import datetime
import logging
import gzip
import firebase_admin
from firebase_admin import credentials, db as admin_db, storage as admin_storage
import json

# Constants
FIREBASE_DOMAIN = "signage-da577"
CLIENT_SECRET_FILE = "signage-da577-firebase-adminsdk-qu9tv-1765d0bcd5.json"

logging.basicConfig(level=logging.INFO)


def initialize_firebase(service_account_file_path, firebase_domain_name):
    """
    Initializes the Firebase Admin SDK.
    :param service_account_file_path: Path to the Firebase service account JSON file.
    :param firebase_domain_name: The Firebase project domain name.
    """
    cred = credentials.Certificate(service_account_file_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"https://{firebase_domain_name}.firebaseio.com",
        'storageBucket': f"{firebase_domain_name}.appspot.com"
    })
    logging.info("Firebase Admin SDK initialized.")


def get_file_names():
    """
    Generates file names for upload and gzip based on the current UTC time.
    The file names follow the pattern:
    - upload name: database_firebase_YYYYMMDDHHMMSS.json
    - gzip name: database_firebase_YYYYMMDDHHMMSS.json.gz

    :return: A tuple containing the upload file name and the gzip file name
    """
    now = datetime.datetime.utcnow()
    upload_name = 'database_firebase_' + now.strftime('%Y%m%d%H%M%S') + '.json'
    gzip_name = upload_name + '.gz'
    return upload_name, gzip_name


def download_database():
    """
    Downloads the entire Firebase Realtime Database.
    :return: The database content as a UTF-8 encoded JSON string.
    """
    logging.info("Fetching data from Firebase Realtime Database...")
    ref = admin_db.reference('/')
    data = ref.get()
    # The data from ref.get() is typically a Python dict or list.
    # It needs to be a JSON string then bytes to be gzipped.
    logging.info("Data fetched successfully.")
    return json.dumps(data, indent=4).encode('utf-8') # Added indent for readability if unzipped


def upload_backup(gzip_name):
    """
    Uploads the gzipped backup file to Firebase Storage.
    :param gzip_name: The name of the gzip file to be uploaded.
    :return: None
    """
    logging.info(f"Uploading {gzip_name} to Firebase Storage...")
    bucket = admin_storage.bucket()
    blob = bucket.blob(f"backups/{gzip_name}")
    blob.upload_from_filename(gzip_name)
    logging.info("Upload completed!")


# Main script execution
if __name__ == "__main__":
    initialize_firebase(CLIENT_SECRET_FILE, FIREBASE_DOMAIN)
    upload_name, gzip_name = get_file_names()
    
    logging.info(f"Generated filenames: {upload_name}, {gzip_name}")
    
    data = download_database()
    
    logging.info(f"Compressing data to {gzip_name}...")
    with gzip.open(gzip_name, 'wb') as f_out:
        f_out.write(data)
    logging.info("Compression complete.")
    
    upload_backup(gzip_name)
    
    logging.info("Backup process finished successfully.")
