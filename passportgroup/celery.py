from celery import shared_task, Celery
from django.conf import settings
import os
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'passportgroup.settings')
app = Celery('passportgroup')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    # Executes every day night at 0:00.
    'delete-notification-with-none-relationship': {
        'task': 'apps.notifications.tasks.delete_notifications_with_none_relation',
        'schedule': crontab(minute=0, hour=0),
    },
}
