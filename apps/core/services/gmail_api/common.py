import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth.transport.requests
from django.conf import settings

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
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("gmail_api_token.pickle"):
        with open("gmail_api_token.pickle", "rb") as token:
            credentials = pickle.load(token)
    # if there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./gmail_credentials.json', SCOPES)
            if os.getenv('APP_ENV') == 'local':
                credentials = flow.run_local_server(port=0)
            else:
                flow.redirect_uri = 'http://5.189.177.4/en/dashboard/mails/'
                credentials = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true'
                )
        # save the credentials for the next run
        with open("gmail_api_token.pickle", "wb") as token:
            pickle.dump(credentials, token)
    return build('gmail', 'v1', credentials=credentials)


def search_messages(service, query):
    query = "from: " + settings.PASSPORT_FROM_EMAIL + " " + query
    print(query)
    result = service.users().messages().list(userId='me', q=query).execute()
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
