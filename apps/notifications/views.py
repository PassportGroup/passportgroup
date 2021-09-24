from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from apps.core.serializers import NotificationSchema
from inertia.views import render_inertia
import json
from django.shortcuts import redirect, reverse, get_object_or_404
from django.utils.timezone import datetime
from datetime import timedelta


@login_required
def notifications_view(request):
    query = request.GET.get('query', None)
    if query:
        today = datetime.today()
        if query == 'read':
            notifications = Notification.objects.filter(recipient=request.user, unread=False).order_by('-timestamp')
        elif query == 'all':
            notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')
        elif query == 'today':
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year = today.year, timestamp__month = today.month, timestamp__day = today.day, unread=True).order_by('-timestamp')
        elif query == 'this week':
            weekdays = [(today + timedelta(days=i)).day for i in range(0 - today.weekday(), 7 - today.weekday())]
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year=today.year, timestamp__month=today.month, timestamp__day__in=weekdays, unread=True).order_by('-timestamp')
        elif query == 'this month':
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year = today.year, timestamp__month = today.month, unread=True).order_by('-timestamp')
        elif query == 'last month':
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year = today.year, timestamp__month = today.month-1, unread=True).order_by('-timestamp')
        elif query == 'this year':
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year = today.year, unread=True).order_by('-timestamp')
        elif query == 'last year':
            notifications = Notification.objects.filter(recipient=request.user, timestamp__year = today.year-1, unread=True).order_by('-timestamp')
    else:
        notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')

    return JsonResponse({
        'notifications': NotificationSchema(many=True).dump(notifications)
    })


def unread_notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')[0:5]
    return JsonResponse({
        'notifications': NotificationSchema(many=True).dump(notifications)
    })


@login_required
def toggle_notification_read_status_view(request):
    if request.method == 'POST':
        notifications_id = json.loads(request.POST.get('notifications_id'))
        unread = json.loads(request.POST.get('unread'))
        Notification.objects.filter(id__in = notifications_id).update(unread= unread)
        notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')

        return JsonResponse({
            'notifications': NotificationSchema(many=True).dump(notifications)
        })


@login_required
def delete_notification_view(request):
    if request.method == 'POST':
        notifications_id = json.loads(request.POST.get('notifications_id'))
        Notification.objects.filter(id__in = notifications_id).delete()

        notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')

        return JsonResponse({
            'notifications': NotificationSchema(many=True).dump(notifications)
        })


@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.unread = False
    notification.save()
    return JsonResponse({}, status=201)

