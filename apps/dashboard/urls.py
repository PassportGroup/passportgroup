from django.urls import path
from .views import *

# app_name = 'dashboard'

urlpatterns = [
    path('', index, name='dashboard.index'),

    # =========== Mails Listing ===========
    path('mails/', mails_index, name='dashboard.mails.index'),
    path('mails/<str:thread_id>/detail/', mails_detail, name='dashboard.mails.detail'),
]



