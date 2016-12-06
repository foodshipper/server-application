import os

from pyfcm import FCMNotification
key = os.environ.get("FIREBASE_KEY")
push_service = FCMNotification(api_key=key)
