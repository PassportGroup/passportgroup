from django.contrib import admin
from .models import PassportMail, PassportGroupTasks


# Register your models here.
class PassportMailAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'to_email',  'subject', 'thread_id', 'date')
    search_fields = ('subject', 'message_id',)
    ordering = ('-date',)


class PassportGroupTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency', 'start_date', 'end_date')
    search_fields = ('name', 'frequency',)
    ordering = ('-name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(PassportMail, PassportMailAdmin)
admin.site.register(PassportGroupTasks, PassportGroupTaskAdmin)
