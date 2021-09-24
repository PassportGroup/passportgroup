from django.dispatch import Signal

passportgroup_notify = Signal(providing_args=[  # pylint: disable=invalid-name
    'recipient', 'notifiable', 'description', 'type'
])