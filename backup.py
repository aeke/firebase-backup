# -*- coding: utf-8 -*-
import uuid,datetime
import httplib2
import pyrebase,logging
import gzip

# Firebase Config
config = {
  "apiKey": "YOUR-API-KEY",
  "authDomain": "YOUR-FIREBASE-DOMAIN.firebaseapp.com",
  "databaseURL": "https://YOUR-FIREBASE-DOMAIN.firebaseio.com",
  "storageBucket": "YOUR-FIREBASE-DOMAIN9.appspot.com",
  "serviceAccount": "YOUR-SECRET-FILE.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

print("\n\n=======================================================")
print("=============| FIREBASE BACKUP TOOL v0.1 |=============")
print("=======================================================\n\nStarting...")

now = datetime.datetime.utcnow()
upload_name = 'database_firebase_' + now.strftime('%Y%m%d%H%M%S') + '.json' 
gzip_name = upload_name + '.gz'

h = httplib2.Http()
firebase_token = auth.create_custom_token(str(uuid.uuid4()))
user = auth.sign_in_with_custom_token(firebase_token)
token = user['idToken']

firebase_url = config['databaseURL'] + '/.json?format=export&auth=' + token

print("Connected Firebase URL ===> " + firebase_url + "\n")

(resp_headers, data) = h.request(firebase_url, "GET")

f_out = gzip.open(gzip_name, 'wb')
f_out.write(data)
f_out.close()

print("Uploading....")
storage.child("backups/" + gzip_name).put(gzip_name)
print("Completed!")
