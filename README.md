# Firebase Database Backup Script

This script downloads the entire Firebase database and uploads it as a GZipped JSON file to Firebase Storage.

## Prerequisites

- Python 3.x
- `pyrebase` library
- `httplib2` library
- `gz` library

## Installation

First, ensure you have Python 3 and pip installed on your machine. Then, install the required Python libraries using pip:

```sh
pip install -r requirements.txt
```

## Configuration

Update the `config` dictionary in the script with your Firebase project information:

```python
config = {
    "apiKey": "YOUR-API-KEY",
    "authDomain": "YOUR-FIREBASE-DOMAIN.firebaseapp.com",
    "databaseURL": "https://YOUR-FIREBASE-DOMAIN.firebaseio.com",
    "storageBucket": "YOUR-FIREBASE-DOMAIN.appspot.com",
    "serviceAccount": "YOUR-CLIENTSECRET-FILE.json"
}
```

Replace the placeholders with your actual Firebase project information.

## Usage

Run the script using Python:

```sh
python backup.py
```

This will:

1. Initialize the Firebase application.
2. Download the database as a JSON file.
3. Compress the JSON file into a GZ file.
4. Upload the GZ file to Firebase Storage.

## Code Explanation

### Function Definitions

- **initialize_firebase(config)**: Initializes the Firebase app and returns database, authentication, and storage objects.
- **get_file_names()**: Generates file names for the JSON and GZ files based on the current UTC time.
- **download_database(auth, config, http_client)**: Downloads the entire database from Firebase using a JWT token for authentication.
- **upload_backup(storage, gzip_name)**: Uploads the GZipped database backup to Firebase Storage.

### Main Script

1. Initialize Firebase:
    ```python
    db, auth, storage = initialize_firebase(config)
    ```
2. Generate file names:
    ```python
    upload_name, gzip_name = get_file_names()
    ```
3. Download the database:
    ```python
    data = download_database(auth, config, httplib2.Http())
    ```
4. Compress the data:
    ```python
    with gzip.open(gzip_name, 'wb') as f_out:
        f_out.write(data)
    ```
5. Upload the backup:
    ```python
    upload_backup(storage, gzip_name)
    ```

## Logging

The script uses the `logging` library to log information about its execution. By default, it logs at the `INFO` level.

## License

This project is licensed under the MIT License.
