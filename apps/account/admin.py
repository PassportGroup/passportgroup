from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('phone', 'username', 'email', 'full_name', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'signup_provider')
    search_fields = ('phone', 'username', 'email')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
