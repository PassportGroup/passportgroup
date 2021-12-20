from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, CredentialsModel


class AccountAdmin(UserAdmin):
    list_display = ('email', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ('id', 'last_login')
    ordering = ('-email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(CredentialsModel, CredentialsAdmin)
