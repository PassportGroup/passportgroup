import inertia.views
from inertia.share import share_flash
from django.contrib.auth.decorators import login_required
from inertia.views import render_inertia
from datetime import datetime, timedelta
from apps.core.services.gmail_api.common import search_messages, get_mail
from apps.core.services.gmail_api.read_emails import read_message
from django.utils.translation import gettext as _
from apps.utils import *
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.http import HttpResponseRedirect
from passportgroup import settings
from apps.account.models import CredentialsModel
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.urls import reverse
import google.auth.transport.requests
from oauth2client.client import flow_from_clientsecrets
from apps.core.services.google_api.common import get_credential
from django.http import JsonResponse

from .models import PassportMail, PassportGroupTask
from .serializers import PassportMailSchema, PassportGroupTaskSchema


SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

FLOW = flow_from_clientsecrets(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scope=SCOPES,
        prompt='consent',
        redirect_uri='http://127.0.0.1:8000/dashboard/oauth/google/callback/',
)


@login_required
def index(request):
    return render_inertia(request, 'Dashboard/Index')


@login_required
def mails_index(request):
    query = request.GET.get('query', None)
    start_date_query = request.GET.get('start_date', None) or datetime.now().strftime('%d %b %Y')
    end_date_query = request.GET.get('end_date', None)
    page = request.GET.get('page', 1)
    begin_date = datetime.strptime(start_date_query, '%d %b %Y')
    end_date = begin_date + timedelta(14)
    if end_date_query:
        end_date = datetime.strptime(end_date_query, '%d %b %Y')

    final_mails = []
    try:
        credentials = get_credential(request)
        gmail_service = build('gmail', 'v1', credentials=credentials)
        print(begin_date)
        print(end_date)
        # Build query from this
        query = "after:" + begin_date.strftime('%Y/%m/%d') + " before:" + end_date.strftime('%Y/%m/%d')
        mails = search_messages(gmail_service, query)
        for mail in mails:
            data = read_message(gmail_service, mail)
            if data:
                # process data on drive
                print(data)
                final_mails.append(data)
    except Exception as e:
        print(str(e))
        share_flash(request, error=_("Error processing mails at this time: ") + str(e))

    # paginate data
    mails_obj, links = paginate(
        objects=final_mails,
        current_url=request.build_absolute_uri(),
        items_per_page=50,
        current_page=page
    )
    return render_inertia(
        request,
        'Dashboard/Mails/Index',
        props={
            'mails': final_mails,
            'query': query,
            'start_date': start_date_query,
            'end_date': end_date_query,
            'links': links
        }
    )


@login_required
def mails_detail(request, thread_id):
    mail = None
    try:
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        credentials = storage.get()
        gmail_service = build('gmail', 'v1', credentials=credentials)
        mail = get_mail(gmail_service, thread_id)
    except Exception as e:
        share_flash(request, error=_("Error processing mails at this time: ") + str(e))

    return render_inertia(
        request,
        'Dashboard/Mails/Details',
        props={
            'mail': mail,
        }
    )


@login_required
def google_auth_callback(request):
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return redirect(reverse('dashboard.index'))


@login_required
def google_authenticate(request, **kwargs):
    if settings.PASSPORT_BASE_EMAIL is None or settings.PASSPORT_FROM_EMAIL is None:
        share_flash(
            request,
            error=_("Please make sure you set correctly the GMAIL_ID and FROM_GMAIL_ID in the .env file")
        )
    else:
        try:
            storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
            credentials = storage.get()
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    request = google.auth.transport.requests.Request()
                    credentials.refresh(request)
                else:
                    authorization_url = FLOW.step1_get_authorize_url()
                    return inertia.views.HttpResponseRedirect(authorization_url)
            else:
                share_flash(request, success=_("Access granted already!"))
        except Exception as e:
            share_flash(request, error=_("Error granting google access: ") + str(e))

    return redirect(reverse('dashboard.index'))


@login_required
def get_tasks_index(request):
    page = request.GET.get('page', None)
    tasks = PassportGroupTask.objects.all().order_by('-created_at')
    passport_tasks_schema = PassportGroupTaskSchema(
        many=True,
        only=('name', 'slug', 'excerpt', 'start_date', 'extra_parameters', 'end_date', 'status', 'created_at',
              'updated_at'),
    )
    if page:
        page_size = request.GET.get('page_size', 20)
        tasks, links = paginate(
            objects=passport_tasks_schema,
            current_url=request.build_absolute_uri(),
            items_per_page=page_size,
            current_page=page
        )
        return JsonResponse({'tasks': passport_tasks_schema.dump(tasks)})

    return render_inertia(
        request,
        'Dashboard/Tasks/Index',
        props={
            'tasks': passport_tasks_schema.dump(tasks),
        }
    )


@login_required
def get_tasks_details(request, slug):
    try:
        task = PassportGroupTask.objects.get(slug=slug)
    except PassportGroupTask.DoesNotExist:
        task = None

    return render_inertia(
        request,
        'Dashboard/Tasks/Details',
        props={
            'task': PassportGroupTaskSchema(exclude=('excerpt',)).dump(task) if task else None,
        }
    )


@login_required
def update_tasks_details(request, slug):
    try:
        task = PassportGroupTask.objects.get(slug=slug)
        if request.POST:
            task.save()
    except PassportGroupTask.DoesNotExist:
        task = None

    return render_inertia(
        request,
        'Dashboard/Tasks/Edit',
        props={
            'task': PassportGroupTaskSchema(exclude=('excerpt',)).dump(task) if task else None,
        }
    )