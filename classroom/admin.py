from django.contrib import admin
from django.utils.html import mark_safe
from django.utils import timezone
from django.db.models import Case, When, Value, BooleanField

from .models import Classroom

# Register your models here.

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['title', 'student_count', 'teacher_link', 'subject',
                    'active', 'start_date', 'end_date']
    list_filter = ['active', 'subject']

    def teacher_link(self, obj):
        teacher = obj.teacher
        url = mark_safe(f'<a href="/admin/users/teacher/{teacher.id}/change/">{teacher}</a>')
        return url

    teacher_link.allow_tags = True
    teacher_link.short_description = 'Teacher'

