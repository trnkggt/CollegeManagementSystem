import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.template.defaultfilters import slugify
from django.forms.models import modelform_factory
from django.apps import apps
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from .forms import CourseCreateForm, ModuleInLine
from .models import Course, Module, Content, Subject
from .utils import is_teacher
from users.models import Teacher

def course_list(request):
    courses = Course.objects.all()

    return render(request, 'courses/course/course_list.html',
                  {'courses': courses})

@csrf_exempt
def subject_list_ajax(request):
    teacher_id = json.loads(request.body.decode("utf-8"))
    if teacher_id:
        teacher = get_object_or_404(Teacher, id=teacher_id)
        subjects = Subject.objects.filter(id__in=teacher.subjects_taught.all())
        subjects_data = [{'name': subject.title, 'id': subject.id} for subject in subjects]

    else:
        subjects = {}
        subjects_data = []

    return JsonResponse({'subjects': subjects_data,
                         'status': 'ok'})

def course_detail(request, pk):
    course = get_object_or_404(Course, id=pk)
    return render(request, 'courses/course/detail.html',
                  {'course': course})


@login_required
@user_passes_test(is_teacher, login_url='home')
def teacher_courses(request):
    """
    Retrieve courses and filter by creator teacher
    """
    courses = Course.objects.filter(teacher=request.user.teacher_profile)
    return render(request, 'courses/course/teachers_courses.html',
                  {'courses': courses})


@login_required
@user_passes_test(is_teacher, login_url='home')
def create_or_update_course(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(Course, id=course_id)
    else:
        course = None

    teacher = request.user.teacher_profile

    if request.method == 'POST':
        form = CourseCreateForm(request.POST, instance=course, teacher=teacher)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher
            course.slug = slugify(course.title)
            course.save()
            # prereqs = form.cleaned_data.get('prerequisites')
            # for prereq in prereqs:
            #     course_code = Course.objects.get(title=prereq)
            #     course.prerequisites.add(course_code)
            form.save_m2m()

            return redirect('teacher_courses')

    else:
        form = CourseCreateForm(instance=course, teacher=teacher)
    return render(request, 'courses/course/create.html', {'form': form,
                                                          })


## Modules
@login_required
@user_passes_test(is_teacher, login_url='home')
def module_detail(request, slug, module_id=None):
    module = get_object_or_404(Module, id=module_id)

    return render(request, 'courses/course/module/list.html',
                  {'module': module})

@login_required
@user_passes_test(is_teacher, login_url='home')
def module_add_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        formset = ModuleInLine(request.POST, instance=course)
        if formset.is_valid():
            formset.save()
            redirect('teacher_courses')
    else:
        formset = ModuleInLine(instance=course)

    return render(request, 'courses/course/module/formset.html',
                  {"formset": formset,
                   'course': course})


@login_required
@user_passes_test(is_teacher)
def content_create(request, model_name, module_id, id=None):

    model = apps.get_model('courses', model_name)
    module = get_object_or_404(Module, id=module_id)
    content = None
    if id:
        content = get_object_or_404(model, id=id)
    modelform = modelform_factory(model, exclude=['teacher',
                                                    'order',
                                                    'created',
                                                    'updated'])
    if request.method == 'POST':
        form = modelform(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form = form.save(commit=False)
            form.module = module
            form.teacher = request.user.teacher_profile
            form.save()
            if not id:
                # If no ID is present in link, create content object
                Content.objects.create(module=module, item=form)

            return redirect('module_detail', module.course.slug, module_id)
    else:
        form = modelform(instance=content)

    return render(request, 'courses/course/module/content/create.html',
                  {'form': form})


@login_required
@csrf_exempt
@require_POST
@user_passes_test(is_teacher)
def delete_content(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
        model = apps.get_model('courses', post_data.get('model'))

        obj = get_object_or_404(model, id=post_data.get('content_id'))
        content = get_object_or_404(Content, object_id=post_data.get('content_id'))

        content.delete()
        obj.delete()
        return JsonResponse({'status': 'ok'})
    except obj.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Content not found'},
                            status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@csrf_exempt
@require_POST
@user_passes_test(is_teacher)
def module_order(request, order_type):
    post_data = json.loads(request.body.decode("utf-8"))
    try:
        if order_type == 'module':
            for id, order in post_data.items():
                Module.objects.filter(id=id).update(order=order)
        elif order_type == 'content':
            for id, order in post_data.items():
                Content.objects.filter(id=id).update(order=order)
    except Exception as e:

        # Handle any database or other unexpected errors
        return JsonResponse({"status": 'error', "message": str(e)})

    return JsonResponse({"status": 'ok'})