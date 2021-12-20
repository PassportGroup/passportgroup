from django.db import models
from django.utils import timezone
# Create your models here.


class PassportMail(models.Model):
    from_email = models.EmailField(verbose_name="From Email", default="muarachmann@gmail.com")
    to_email = models.EmailField(verbose_name="To Email", default="passportgroup.api@gmail.com")
    message_id = models.CharField(verbose_name="Message ID", max_length=200, unique=True)
    subject = models.CharField(verbose_name="Message ID", max_length=300, blank=True, null=True)
    thread_id = models.CharField(verbose_name="Message ID", max_length=200)
    snippet = models.TextField(verbose_name="Snippet", blank=True, null=True)
    date = models.DateTimeField(verbose_name='Date', default=timezone.now)


class PassportGroupTasks(models.Model):
    name = models.CharField(verbose_name="name", max_length=50, unique=True)
    timezone = models.CharField(verbose_name="timezone", max_length=200, default='UTC')
    frequency = models.CharField(verbose_name="frequency", max_length=300, default='* * * * *')
    parameters = models.JSONField(verbose_name='parameters', blank=True, null=True)
    email_notifications = models.EmailField(verbose_name='email_notifications', default='office@passport.co.il')
    slack_url = models.CharField(verbose_name='slack_url', max_length=500, blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='start at', auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='end at', auto_now_add=True)

