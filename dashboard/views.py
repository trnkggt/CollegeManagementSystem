from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Case, When, Value, BooleanField

from classroom.models import Classroom
from users.models import Teacher, StudentProfile

# Create your views here.

@login_required
@user_passes_test(lambda obj: obj.is_staff)
def admin_dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
@user_passes_test(lambda obj: obj.is_staff)
def admin_dashboard_classes(request):
    """
    retrieve all classrooms and annotate queryset with 'graduated'
    to order classes which by graduation
    """
    classes = Classroom.objects.all() or None
    filtered = classes.annotate(graduated=Case(
        When(end_date__lt=timezone.now(), then=Value(True)),
        default=Value(False),
        output_field=BooleanField()
    )).order_by('graduated')

    return render(request, 'dashboard/classrooms.html',
                  {'classrooms': filtered})

@login_required
@user_passes_test(lambda obj: obj.is_staff)
def teacher_list(request, subject=None):
    teachers = Teacher.objects.all()
    if subject is not None:
        teachers = teachers.filter(subjects_taught__title=subject)

    return render(request, 'dashboard/teachers.html',
                  {'teachers': teachers})


@login_required
@user_passes_test(lambda obj: obj.is_staff)
def student_list(request):
    students = StudentProfile.objects.all()
    return render(request, 'dashboard/students.html',
                  {'students': students})

@login_required
@user_passes_test(lambda obj: obj.is_staff)
def teacher_classrooms(request, teacher_id):
    classrooms = Classroom.objects.filter(teacher__id=teacher_id)

    return render(request, 'dashboard/classrooms.html',
                  {'classrooms': classrooms})