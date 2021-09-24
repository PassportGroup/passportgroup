import logging
from django.conf import settings
from django.contrib.auth import get_user_model

from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver
from django.utils import timezone
from swapper import load_model
from .types import get_notification_configuration, NOTIFICATION_TYPES
from . import tasks
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from apps.core.serializers import NotificationSchema
from apps.core.services.pusher import Pusher
logger = logging.getLogger(__name__)

User = get_user_model()

Notification = load_model('apps.notifications', 'Notification')
NotificationSetting = load_model('apps.notifications', 'NotificationSetting')

def notify_handler(**kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    sender = kwargs.pop('sender', None)
    notifiable = kwargs.pop('notifiable', None)
    description = kwargs.pop('description', None)
    timestamp = kwargs.pop('timestamp', timezone.now())
    recipient = kwargs.pop('recipient', None)
    notification_type = kwargs.pop('type')

    if not isinstance(sender, User):
        sender = None

    if recipient:
        # Check if recipient is User, Group or QuerySet
        if isinstance(recipient, Group):
            recipients = User.objects.filter(groups__name = recipient.name)
        elif isinstance(recipient, (QuerySet, list)):
            recipients = recipient
        else:
            recipients = [recipient]

    else:
        recipients = (
            User.objects.prefetch_related(
                'notificationsetting_set'
            )
            .order_by('date_joined')
            .exclude(is_active=False)
        )

    notification_list = []
    for recipient in recipients:
        notification = Notification(
            recipient=recipient,
            description=description,
            sender=sender,
            timestamp=timestamp,
            type=notification_type,
        )

        # Set optional objects
        if notifiable:
            setattr(notification, 'notifiable_id', notifiable.pk)
            setattr(notification, 'notifiable_type', ContentType.objects.get_for_model(notifiable))

        notification.save()
        notification_list.append(notification)

    return notification_list


@receiver(post_save, sender=Notification, dispatch_uid='send_notification')
def send_notification(sender, instance, created, **kwargs):
    # Abort if a new notification is not created
    if not created:
        return

    email_preference = False
    sms_preference = False
    web_preference = False

    if instance.type:
        notification_setting = NotificationSetting.objects.filter(user = instance.recipient, type = instance.type).first()
        if notification_setting:
            email_preference = notification_setting.email_notification
            sms_preference = notification_setting.sms_notification
            web_preference = notification_setting.web_notification

    data = NotificationSchema().dump(instance)
    if data['type'] in ['message', 'offer']:
        pusher = Pusher()
        pusher.trigger_new_message(data['recipient']['username'])

    site = Site.objects.get_current()
    protocol = 'http' if settings.DEBUG else 'https'
    context = {
        'data': data,
        'site': {
            'domain': site.domain,
            'name': site.name,
        },
        'protocol': protocol,
    }

    if data['type'] == 'follower':
        if data['sender'] and data['sender']['url']:
            target_url = data['sender']['url']
            context['target_url'] = f'{protocol}://{site.domain}{target_url}'
            del data['sender']['url']

    else:
        if data['notifiable'] and data['notifiable']['url']:
            target_url = data['notifiable']['url']
            context['target_url'] = f'{protocol}://{site.domain}{target_url}'
            del data['notifiable']['url']

    tasks.send_notifications.delay(sms_preference, email_preference, web_preference, instance.id, context)


@receiver(post_save, sender=User, dispatch_uid='user_notification_setting')
def notification_setting_user_created(instance, created, **kwargs):
    if created:
        notification_types = NOTIFICATION_TYPES.keys()
        notification_settings = []
        for notification_type in notification_types:
            notification_settings.append(
                NotificationSetting(
                    user=instance, type=notification_type, web=NOTIFICATION_TYPES[notification_type]['web_notification'], email=NOTIFICATION_TYPES[notification_type]['email_notification'], sms=NOTIFICATION_TYPES[notification_type]['sms_notification']
                )
            )

        NotificationSetting.objects.bulk_create(
            notification_settings, ignore_conflicts=True
        )
    return


@receiver(post_save, sender=Notification, dispatch_uid='reload_notification_saved')
@receiver(post_delete, sender=Notification, dispatch_uid='reload_notification_deleted')
def reload_notification(sender, instance, **kwargs):
    # Reload notification only if notification is created or deleted
    # Display when a new notification is created
    pass


