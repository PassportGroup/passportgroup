from oauth2client.contrib.django_util.storage import DjangoORMStorage
from apps.account.models import CredentialsModel

# Request all access (permission to read/send/receive emails, manage the inbox, and drive)
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]


def check_credential(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    return True if credential and not credential.invalid else False


def get_credential(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    return credential if credential else None

