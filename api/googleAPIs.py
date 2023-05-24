import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def getDataFromGoogleDocs(document_id, token, refresh_token, client_id, client_secret):
    creds = Credentials