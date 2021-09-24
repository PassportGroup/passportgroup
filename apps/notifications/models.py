from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from apps.notifications.utils import id2slug
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from swapper import swappable_setting

from .types import (
    NOTIFICATION_CHOICES,
    get_notification_configuration
)

User = get_user_model()


def is_soft_delete():
    return True


def assert_soft_delete():
    if not is_soft_delete():
        # msg = """To use 'deleted' field, please set 'SOFT_DELETE'=True in settings.
        # Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
        # """
        msg = 'REVERTME'
        raise ImproperlyConfigured(msg)


class NotificationQuerySet(models.Manager):
    ''' Notification QuerySet '''
    def unsent(self):
        return self.filter(emailed=False)

    def sent(self):
        return self.filter(emailed=True)

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=True, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=True)

    def count_unread(self, recipient):
        return self.filter(unread=True, recipient = recipient, deleted=False).count()

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=False, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qset = self.unread(True)
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        qset = self.read(True)

        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=True)

    def deleted(self):
        """Return only deleted items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=True)

    def active(self):
        """Return only active(un-deleted) items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        """Mark current queryset as deleted.
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.active()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=True)

    def mark_all_as_active(self, recipient=None):
        """Mark current queryset as active(un-deleted).
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.deleted()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=False)

    def mark_as_unsent(self, recipient=None):
        qset = self.sent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=False)

    def mark_as_sent(self, recipient=None):
        qset = self.unsent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=True)

class Notification(models.Model):

    recipient = models.ForeignKey(User, blank=False, related_name='recipient_notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, blank=True, null=True, related_name='sender_notifications', on_delete=models.CASCADE)

    notifiable_type = models.ForeignKey(ContentType, related_name='notifiable', blank=True, null=True, on_delete=models.CASCADE)
    notifiable_id = models.CharField(max_length=255, blank=True, null=True)
    notifiable = GenericForeignKey('notifiable_type', 'notifiable_id')

    unread = models.BooleanField(default=True, blank=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=30, null=True, choices=NOTIFICATION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)

    data = models.JSONField(blank=True, null=True)
    objects = NotificationQuerySet()


    class Meta:
        ordering = ('-timestamp',)
        app_label = 'apps.notifications'
        # speed up notifications count query
        index_together = ('recipient', 'unread')

    def __str__(self):
        ctx = {
            'type': self.type,
            'timesince': self.timesince()
        }
        return u'new %(type)s nofication %(timesince)s ago' % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

class NotificationSetting(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=30,
        null=True,
        choices=NOTIFICATION_CHOICES,
        verbose_name='Notification Type',
    )
    web = models.BooleanField(
        _('web notifications'), null=True, blank=True
    )
    email = models.BooleanField(
        _('email notifications'), null=True, blank=True
    )
    sms = models.BooleanField(
        _('sms notifications'), null=True, blank=True
    )

    class Meta:
        verbose_name = _('user notification settings')
        verbose_name_plural = verbose_name
        ordering = ['type']
        app_label = 'apps.notifications'

    def __str__(self):
        return '{user} subscribed for {type} notification'.format(
            type=self.type_config['verbose_name'], user=self.user.username
        )

    def save(self, *args, **kwargs):
        if not self.web_notification:
            self.email = self.web_notification
        return super().save(*args, **kwargs)

    @property
    def type_config(self):
        return get_notification_configuration(self.type)

    @property
    def email_notification(self):
        if self.email is not None:
            return self.email
        return self.type_config.get('email_notification')

    @property
    def web_notification(self):
        if self.web is not None:
            return self.web
        return self.type_config.get('web_notification')

    @property
    def sms_notification(self):
        if self.sms is not None:
            return self.sms
        return self.type_config.get('sms_notification')



