from django.urls import path, include
from .views import *

urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('unread/', unread_notification_view, name='notifications.unread'),
    path('mark/as/read/<int:notification_id>', mark_notification_as_read, name='notification.mark.as.read'),
    path('toggle/read/status/', toggle_notification_read_status_view, name='notifications.toggle.read.status'),
    path('delete/', delete_notification_view, name='notifications.delete'),
]


