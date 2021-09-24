from django.urls import path, include
from .views import *

urlpatterns = [
    path('settings/', settings_view, name='settings'),
    path('password/change', password_change_view, name='password.change'),
    path('notifications/settings/', notifications_view, name='notifications.settings'),
    path('delete/', delete_account_view, name='delete.account'),
    path('security/', security_view, name='account.security'),
]



