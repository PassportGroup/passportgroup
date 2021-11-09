from django.shortcuts import render
from django.http import HttpResponse
from inertia.share import share_flash
from django.contrib.auth.decorators import login_required
from inertia.views import render_inertia
from datetime import datetime, timedelta
from apps.core.services.gmail_api.common import gmail_authenticate, search_messages, get_mail
from apps.core.services.gmail_api.read_emails import read_message
from django.utils.translation import gettext as _
from apps.utils import *


@login_required
def index(request):

    return render_inertia(request, 'Dashboard/Index')


@login_required
def mails_index(request):
    query = request.GET.get('query', None)
    start_date_query = request.GET.get('start_date', None) or datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_date_query = request.GET.get('end_date', None)
    page = request.GET.get('page', 1)

    begin_date = datetime.strptime(start_date_query, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_date = begin_date + timedelta(14)
    if end_date_query:
        end_date = datetime.strptime(end_date_query, '%Y-%m-%dT%H:%M:%S.%fZ')

    final_mails = []
    try:
        gmail_service = gmail_authenticate()
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
        gmail_service = gmail_authenticate()
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


