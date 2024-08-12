import firebase_admin
from firebase_admin import credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        "serviceAccountKey.json",
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    credentials.refresh(Request())
    return credentials.token
