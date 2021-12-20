from django.urls import path
from .views import *

# app_name = 'dashboard'

urlpatterns = [
    path('', index, name='dashboard.index'),
    path('oauth/google/', google_authenticate, name='dashboard.google.auth'),
    path('oauth/google/callback/', google_auth_callback,  name='dashboard.google.callback'),

    # =========== Mails Listing ===========
    path('mails/', mails_index, name='dashboard.mails.index'),
    path('mails/<str:thread_id>/detail/', mails_detail, name='dashboard.mails.detail'),

    path('tasks', get_tasks_index, name='dashboard.tasks.index'),
    path('tasks/<str:slug>/', get_tasks_details, name='dashboard.tasks.detail'),
    path('tasks/<str:slug>/update/', get_tasks_details, name='dashboard.tasks.update'),
]



