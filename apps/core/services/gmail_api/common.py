import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from django.conf import settings
import google.oauth2.credentials
import google_auth_oauthlib.flow

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

if settings.PASSPORT_BASE_EMAIL is None or settings.PASSPORT_FROM_EMAIL is None:
    print("Please make sure you set correctly the GMAIL_ID and FROM_GMAIL_ID in the .env file")
    exit()


def gmail_authenticate():
    credentials = None

    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'gmail_credentials.json', scopes=SCOPES)
    flow.redirect_uri = ' http://127.0.0.1:8000/'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    print(authorization_url)
    print(state)
    # return build('gmail', 'v1', credentials=credentials)


def search_messages(service, query):
    query = "from: " + settings.PASSPORT_FROM_EMAIL + " " + query
    print(query)
    result = service.users().messages().list(userId='me', q=query).execute()
    print(result)
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def get_mail(service, thread_id):
    mail = service.users().messages().get(userId='me', id=thread_id, format='full').execute()
    return mail
