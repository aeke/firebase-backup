This simple Python tool can be used to backup your Firebase database. It backs up your database with a specific timestamp and uploads it to Firebase Storage.

## Usage

1. Update your Firebase Config settings in the `backup.py` file.
2. Run the `backup.py` file using Python 3.x.
3. After the backup process is complete, you can find your backup in Firebase Storage.

## Requirements

- Python 3.x
- httplib2
- pyrebase

## Firebase Config Settings

You should update your Firebase Config settings in the `backup.py` file as follows:

```python
firebase_config = {
    "apiKey": "YOUR-API-KEY",
    "authDomain": "YOUR-FIREBASE-DOMAIN.firebaseapp.com",
    "databaseURL": "https://YOUR-FIREBASE-DOMAIN.firebaseio.com",
    "storageBucket": "YOUR-FIREBASE-DOMAIN.appspot.com",
    "serviceAccount": "YOUR-CLIENTSECRET-FILE.json"
}
