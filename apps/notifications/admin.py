from django.contrib import admin

from .models import Notification, NotificationSetting


class NotificationAdmin(admin.ModelAdmin):
	model = Notification


class NotificationSettingAdmin(admin.ModelAdmin):
	model = NotificationSetting


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
