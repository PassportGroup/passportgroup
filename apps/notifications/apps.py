from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'
    label = 'apps.notifications'

    def ready(self):
        from .handler import notify_handler
        from .signals import passportgroup_notify

        passportgroup_notify.connect(
            notify_handler, dispatch_uid='notifications.models.notification'
        )

