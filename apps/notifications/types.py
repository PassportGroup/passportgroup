from django.core.exceptions import ImproperlyConfigured

NOTIFICATION_TYPES = {
    'message': {
        'verbose_name': 'New Message',
        'subject_template': 'notifications/subjects/{lang}/new_message.html',
        'sms_template': 'notifications/sms/{lang}/new_message.txt',
        'email_template': 'notifications/email/{lang}/new_message.html',
        'email_notification': True,
        'web_notification': True,
        'sms_notification': True,
    },
    'listing': {
        'verbose_name': 'New Mail',
        'subject_template': 'notifications/subjects/{lang}/new_listing.html',
        'sms_template': 'notifications/sms/{lang}/new_listing.txt',
        'email_template': 'notifications/email/{lang}/new_listing.html',
        'email_notification': True,
        'web_notification': True,
        'sms_notification': True,
    },
}

NOTIFICATION_CHOICES = [
    ('message', 'New Message'),
    ('offer', 'New Offer'),
    ('follower', 'New Follower'),
    ('listing', 'New Listing'),
    ('transaction', 'New Transaction'),
    ('identification', 'New Identification'),
]


def get_notification_configuration(notification_type):
    if not notification_type:
        return {}
    try:
        return NOTIFICATION_TYPES[notification_type]
    except KeyError:
        raise ImproperlyConfigured(f'No such Notification Type, {notification_type}')


