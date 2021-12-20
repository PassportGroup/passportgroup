from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from apps.utils import unique_slug_gen
from django.dispatch import receiver


class PassportMail(models.Model):
    from_email = models.EmailField(verbose_name="From Email", default="muarachmann@gmail.com")
    to_email = models.EmailField(verbose_name="To Email", default="passportgroup.api@gmail.com")
    message_id = models.CharField(verbose_name="Message ID", max_length=200, unique=True)
    subject = models.CharField(verbose_name="Message ID", max_length=300, blank=True, null=True)
    thread_id = models.CharField(verbose_name="Message ID", max_length=200)
    snippet = models.TextField(verbose_name="Snippet", blank=True, null=True)
    date = models.DateTimeField(verbose_name='Date', default=timezone.now)

    class Meta:
        verbose_name = "Mail"
        verbose_name_plural = "Mails"


class PassportGroupTask(models.Model):
    STATUS_CHOICES = [
        ('running', 'running'),
        ('paused', 'paused'),
        ('stopped', 'stopped'),
    ]
    name = models.CharField(verbose_name="name", max_length=50, unique=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    cron_expression = models.CharField(verbose_name="Cron Expression", max_length=300, default='* * * * *')
    parameters = models.JSONField(verbose_name='parameters', blank=True, null=True)
    status = models.CharField(verbose_name='Status', max_length=10, choices=STATUS_CHOICES, default='stopped')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    email_notifications = models.EmailField(verbose_name='email_notifications', default='office@passport.co.il')
    slack_url = models.CharField(verbose_name='slack_url', max_length=500, blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='start at', default=timezone.now)
    end_date = models.DateTimeField(verbose_name='end at', default=timezone.now)
    created_at = models.DateTimeField(verbose_name='created at', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='updated at', default=timezone.now)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


@receiver(pre_save, sender=PassportGroupTask)
def cat_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_gen(instance.name, instance)
