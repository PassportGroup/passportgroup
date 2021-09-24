from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from swapper import load_model
from apps.core.serializers import NotificationSchema
from django.template.loader import render_to_string
from apps.notifications.types import get_notification_configuration, NOTIFICATION_TYPES
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from apps.core.services.pusher import Pusher
from celery.utils.log import get_task_logger
import os
User = get_user_model()
Notification = load_model('apps.notifications', 'Notification')
NotificationSetting = load_model('apps.notifications', 'NotificationSetting')
from time import sleep
logger = get_task_logger(__name__)

@shared_task
def send_email_notifications(subject_template, email_template, context, to, send_after = 600, email_from = None):
    """
    Send notifications.
    """
    sleep(send_after)
    logger.info("Sending email notifications")
    subject = render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    message = render_to_string(email_template, context)

    if subject and message and subject != '' and message != '':
        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=os.getenv('MAIL_FORM_ADDRESS_NOTIFICATION', 'noreply@passportgroup.il.co')
            if not email_from else email_from,
            to=[to],
        )
        mail.content_subtype = 'html'
        mail.send()

@shared_task
def send_notifications(email, web, notification_id, context):
    """
    Send notifications.
    """
    instance = Notification.objects.filter(id=notification_id).first()

    if instance:
        if email and instance.recipient.email:
            send_email_notifications.delay(
                get_notification_configuration(instance.type)['subject_template'].format(lang=instance.recipient.locale),
                get_notification_configuration(instance.type)['email_template'].format(lang=instance.recipient.locale),
                context,
                instance.recipient.email,
            )

        if web:
            logger.info('sending web notification')
            pusher = Pusher()
            pusher.trigger_notifications(instance.recipient.username, context['data'])


@shared_task
def delete_obsolete_objects(instance_app_label, instance_model, instance_id):
    """
    Delete Notification objects having instance as related objects..
    """
    try:
        instance_content_type = ContentType.objects.get_by_natural_key(
            instance_app_label, instance_model
        )
    except ContentType.DoesNotExist:
        return
    else:
        # Delete Notification objects
        where = (
            Q(actor_content_type=instance_content_type)
            | Q(action_object_content_type=instance_content_type)
            | Q(target_content_type=instance_content_type)
        )
        where = where & (
            Q(actor_object_id=instance_id)
            | Q(action_object_object_id=instance_id)
            | Q(target_object_id=instance_id)
        )
        Notification.objects.filter(where).delete()


@shared_task
def delete_notification(notification_id):
    Notification.objects.filter(pk=notification_id).delete()


@shared_task
def delete_old_notifications(days):
    """
    Delete notifications having 'timestamp' more than "days" days.
    """
    Notification.objects.filter(
        timestamp__lte=timezone.now() - timedelta(days=days)
    ).delete()


# Following shared_tasks updates notification settings in database.
# 'ns' is short for notification_setting
@shared_task
def ns_user_created(instance_id, is_created):
    """
        Adds notification setting for all notification types.
    """
    notification_types = NOTIFICATION_TYPES.keys()

    notification_settings = []
    for type in notification_types:
        notification_settings.append(
            NotificationSetting(
                user_id=instance_id, type=type
            )
        )

    NotificationSetting.objects.bulk_create(
        notification_settings, ignore_conflicts=True
    )


@shared_task
def ns_register_unregister_notification_type(
    notification_type=None, delete_unregistered=True
):
    """
    Creates notification setting for registered notification types.
    Deletes notification for unregistered notification types.
    """

    notification_types = (
        [notification_type] if notification_type else NOTIFICATION_TYPES.keys()
    )
    notification_settings = []

    for type in notification_types:
        for user in User.objects.filter(is_superuser=True):
            notification_settings.append(
                NotificationSetting(user=user, type=type)
            )

    NotificationSetting.objects.bulk_create(
        notification_settings, ignore_conflicts=True
    )

    if delete_unregistered:
        # Delete all notification settings for unregistered notification types
        NotificationSetting.objects.exclude(type__in=notification_types).delete()
        # Delete notifications related to unregister notification types
        Notification.objects.exclude(type__in=notification_types).delete()


@shared_task
def delete_notifications_with_none_relation():
    notifications = Notification.objects.all()
    for notification in notifications:
        if notification.notifiable is None and notification.type != 'follower':
            notification.delete()


