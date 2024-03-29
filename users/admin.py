from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect

from .forms import UserAdminUpdateForm
from .models import CustomUser, StudentProfile, Teacher


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'last_name', 'account_type', 'date_of_birth',
                    'email', 'is_staff', 'is_active', 'view_user_link')
    list_editable = ['is_active',]
    form = UserAdminUpdateForm
    def view_user_link(self, obj):
        # Generate a link to the user's detail page
        url = reverse(
            "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
            args=[obj.id])
        return format_html('<a href="{}">View</a>', url)

    view_user_link.short_description = 'View User'


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
        'is_active', 'is_staff', 'is_superuser', 'groups',
        'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_of_birth')}),
        ('Send an email', {'fields': ('email_subject', 'email_body')}),
    )
    ordering = ('email',)


@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    list_display = ['user', 'has_graduated',
              'enrolled']
    list_filter = ['has_graduated', 'enrolled']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user']

    list_filter = ['subjects_taught']
