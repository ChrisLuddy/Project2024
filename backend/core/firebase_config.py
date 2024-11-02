# core/firebase_config.py
import firebase_admin
from firebase_admin import firestore
from django.conf import settings

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
