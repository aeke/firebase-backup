# -*- coding: utf-8 -*-
import uuid
import datetime
import httplib2
import pyrebase
import logging
import gzip

# Constants
FIREBASE_DOMAIN = "signage-da577"
CLIENT_SECRET_FILE = "signage-da577-firebase-adminsdk-qu9tv-1765d0bcd5.json"

# Firebase Config
config = {
    "apiKey": "AIzaSyC0vpvpaaETB5HdAvx4j-mHLGwOJHzh7TM",
    "authDomain": f"{FIREBASE_DOMAIN}.firebaseapp.com",
    "databaseURL": f"https://{FIREBASE_DOMAIN}.firebaseio.com",
    "storageBucket": f"{FIREBASE_DOMAIN}.appspot.com",
    "serviceAccount": CLIENT_SECRET_FILE
}

logging.basicConfig(level=logging.INFO)


def initialize_firebase(config):
    """
    :param config: Dictionary containing Firebase configuration settings.
    :return: Tuple containing Firebase database, authentication, and storage objects.
    """
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    auth = firebase.auth()
    storage = firebase.storage()
    return db, auth, storage


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


def download_database(auth, config, http_client):
    """
    :param auth: Firebase authentication client for creating and signing JWT tokens.
    :param config: Dictionary containing configuration settings, particularly the Firebase database URL.
    :param http_client: HTTP client used for making requests to external services.
    :return: The data extracted from the Firebase database.
    """
    firebase_token = auth.create_custom_token(str(uuid.uuid4()))
    user = auth.sign_in_with_custom_token(firebase_token)
    token = user['idToken']
    firebase_url = config['databaseURL'] + '/.json?format=export&auth=' + token
    logging.info(f"Connected Firebase URL ===> {firebase_url}")
    resp_headers, data = http_client.request(firebase_url, "GET")
    return data



def upload_backup(storage, gzip_name):
    """
    :param storage: Storage object to handle the upload process.
    :param gzip_name: The name of the gzip file to be uploaded.
    :return: None
    """
    logging.info("Uploading....")
    storage.child(f"backups/{gzip_name}").put(gzip_name)
    logging.info("Completed!")


# Main script
db, auth, storage = initialize_firebase(config)
upload_name, gzip_name = get_file_names()
data = download_database(auth, config, httplib2.Http())
with gzip.open(gzip_name, 'wb') as f_out:
    f_out.write(data)
upload_backup(storage, gzip_name)
