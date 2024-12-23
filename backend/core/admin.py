# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import Group
from .models import User
from django.utils.translation import gettext_lazy as _


admin.site.unregister(Group)
admin.site.site_header = _("Agentic Corporate Trader web site administration")
admin.site.site_title = _("Agentic Corporate Trader Admin")
admin.site.index_title = _("Welcome to Agentic Corporate Trader Admin")

class CustomUserAdmin(UserAdmin):
    # Fields that will be displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    # Fields that will be displayed when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Display fields in the admin list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
