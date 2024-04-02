import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Count, Q


from .forms import ClassroomForm
from .models import Classroom
from courses.utils import is_teacher
from courses.models import Course, Module
from quizes.models import QuizResults
from users.models import CoursePassing

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_edit_classroom(request, classroom_id=None):

    instance = None
    if classroom_id:
        instance = get_object_or_404(Classroom, id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            return redirect('classroom:classroom_list')
    else:
        form = ClassroomForm(instance=instance)

    return render(request, 'classroom/create_edit.html',
                  {'form': form})


@login_required
def classroom_list(request):
    classes = Classroom.objects.filter(start_date__gt=timezone.now()) or None

    return render(request, 'classroom/classroom_list.html',
                  {'classrooms': classes})

@login_required
@user_passes_test(is_teacher)
def teacher_classroom(request):
    """
    Filter classrooms based on teacher
    """

    classes = Classroom.objects.filter(start_date__gt=timezone.now()).filter(
        teacher=request.user.teacher_profile
    )

    return render(request, 'classroom/teachers/teachers_classroom.html',
                  {'classrooms': classes})

@login_required
@user_passes_test(is_teacher)
def classroom_details(request, classroom_id):
    """
    Detail view for classroom for teacher
    """
    classroom = get_object_or_404(Classroom, id=classroom_id)

    return render(request, 'classroom/teachers/classroom_detail.html',
                  {'classroom': classroom})


def classroom_details_students(request, classroom_id):
    """
    Detail view for Student accounts
    """
    classroom = get_object_or_404(Classroom, id=classroom_id)
    return render(request, 'classroom/classroom_detail_students.html',
                  {"classroom": classroom})

@login_required
@user_passes_test(is_teacher)
def get_teacher_course_list(request, classroom_id):
    """
    Get all the courses by current teacher
    """
    courses = list(Course.objects.filter(teacher=request.user.teacher_profile).values())
    data = [i['title'] for i in courses]
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_teacher)
@require_POST
def enroll_classroom(request, classroom_id):
    try:
        course_title = json.loads(request.body)
        course = get_object_or_404(Course, title=course_title)
        classroom = get_object_or_404(Classroom, id=classroom_id)

        # Check if classroom is already enrolled and course is the same one
        # In that case do nothing
        if classroom.course and classroom.course == course:
            pass
        else:
            classroom.course = course
            classroom.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)

@login_required
@require_POST
def enroll_student(request, classroom_id):
    try:
        classroom = get_object_or_404(Classroom, id=classroom_id)
        student_profile = request.user.student_profile
        classroom.students.add(student_profile)
        student_profile.enrolled = True
        student_profile.classroom = classroom
        classroom.save()
        student_profile.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "error", "message": "An error occurred"}, status=500)


@login_required
@user_passes_test(lambda user: user.student_profile.enrolled==True)
def classroom_modules(request, classroom_id, module_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    module = get_object_or_404(Module, id=module_id)

    return render(request, "classroom/module/module_details.html",
                  {"classroom": classroom,
                   "module": module})

@login_required
@user_passes_test(lambda user: user.student_profile.enrolled==True)
def student_results(request):
    results = QuizResults.objects.filter(student=request.user.student_profile)

    return render(request, "classroom/module/student_results.html",
                  {"student_results": results})

@login_required
def graduate_student(request, course_id, classroom_id):
    # remove student from classroom
    # add course to courses_passed
    course = get_object_or_404(Course, id=course_id)
    classroom = get_object_or_404(Classroom, id=classroom_id)

    student = request.user.student_profile
    results = QuizResults.objects.filter(student=student).values(
        'student').annotate(
        total=Count('id'),
        passed_count=Count('id', filter=Q(passed=True)),
    )
    passed = results[0]['total'] == results[0]['passed_count']
    classroom.students.remove(student)
    student.enrolled = False
    student.classroom = None
    data = {
        "student": student,
        "course": course,
        "passed": passed,
        "score": results[0]['passed_count'] * 10
    }
    if passed:
        CoursePassing.objects.create(**data)

    ## send mail using celery

    messages.info(request, "Congratulations on your graduation, email has been sent to you.",)
    student.save()


    return redirect("home")