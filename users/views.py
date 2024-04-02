from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.conf import settings
from django.utils.http import urlsafe_base64_decode

from .tokens import email_verification_token
from .forms import NewUserForm, CustomAuthForm, ProfileForm, UserUpdateForm, TeacherProfileForm
from .models import StudentProfile, Teacher, CustomUser
from .tasks import confirmation
from courses.utils import is_teacher

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            if user_type == 'S':
                user = form.save(commit=False)
                user.first_name = user.first_name.title()
                user.last_name = user.last_name.title()
                user.user_type = user_type
                user.is_active = False
                user.save()

                StudentProfile.objects.create(user=user)

                current_site = get_current_site(request)
                confirmation.apply_async(args=(user.id, current_site.domain),
                                         countdown=10)

                notification = ('Email verification URL sent, please check your'
                                ' email inbox.')
                # login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                messages.info(request, 'Email verification URL sent, please check your'
                                ' email inbox.')
                return render(request, 'users/home.html',
                              {'notification': notification})
            else:
                teacher = form.save(commit=False)
                teacher.is_active = False
                teacher.user_type = user_type
                teacher.save()
                Teacher.objects.create(user=teacher)
                messages.info(request, 'Teacher verification request '
                                       'sent to admin, you will get confirmation'
                                       ' on email')
                return render(request, 'users/home.html')

    else:
        form = NewUserForm()

    return render(request,
                  'auth/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

        notification = 'Your account is now verified, and you are logged in'
        messages.info(request, notification)
        return render(request, 'users/home.html')
    else:
        notification = 'Invalid activation link'
        messages.info(request, notification)
        return render(request, 'users/home.html')

# Student authentication
def login_user(request):
    if request.user.is_authenticated:
        return render(request, 'users/logged_in.html')
    if request.method == 'POST':
        form = CustomAuthForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'users/home.html')

    else:
        form = CustomAuthForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return render(request, 'auth/logged_out.html')



# Teacher/Student profile

@login_required
def student_edit_profile(request):
    student_page = get_object_or_404(StudentProfile, user=request.user)
    old_profile_pic = student_page.profile_picture
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        image_form = ProfileForm(request.POST, request.FILES, instance=student_page)

        if form.is_valid() and image_form.is_valid():
            form.save()
            if image_form.cleaned_data['profile_picture'] == old_profile_pic:
                image_form.cleaned_data.pop('profile_picture')
                image_form.save()
            else:
                image = image_form.save(commit=False)
                first_name = user.first_name
                last_name = user.last_name
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                image.profile_picture.name = f'{first_name}_{last_name}_{timestamp}.jpg'
                image.save()
            messages.success(request, 'Your profile has been updated successfully.')

            # return render(request, 'users/edit_profile.html',
            #               {'form': form, 'student': student_page,
            #                'image_form': image_form})
            return redirect('.')

    else:
        form = UserUpdateForm(instance=user)
        image_form = ProfileForm(instance=student_page)
    return render(request, 'users/students/edit_profile.html',
                  {'form': form,
                            'student': student_page,
                            'image_form': image_form})

def student_profile(request, user_id):
    student = get_object_or_404(StudentProfile, id=user_id)

    return render(request, 'users/students/student_profile.html',
                  {'student': student})

@login_required
@user_passes_test(is_teacher)
def teacher_edit_profile(request):
    teacher_page = get_object_or_404(Teacher, user=request.user)
    teacher = get_object_or_404(CustomUser, pk=request.user.id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=teacher)
        teacher_form = TeacherProfileForm(request.POST,
                                          request.FILES,
                                          instance=teacher_page)
        if form.is_valid() and teacher_form.is_valid():
            form.save()
            if teacher_form.cleaned_data['profile_picture'] == teacher_page.profile_picture:
                teacher_form.cleaned_data.pop('profile_picture')
                teacher_form.save()
            else:
                teacher_form = teacher_form.save(commit=False)
                first_name = teacher.first_name
                last_name = teacher.last_name
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                teacher_form.profile_picture.name = f'{first_name}_{last_name}_{timestamp}.jpg'
                teacher_form.save()
            messages.info(request, 'Updated successfully')
            # return render(request, 'users/teachers/edit_profile.html',
            #               {'form': form,
            #                'teacher_form': teacher_form,
            #                'teacher': teacher_page})
            return redirect('.')
    else:
        form = UserUpdateForm(instance=teacher)
        teacher_form = TeacherProfileForm(instance=teacher_page)

    return render(request, 'users/teachers/edit_profile.html',
                  {'form': form, 'teacher_form': teacher_form,
                   'teacher': teacher_page})

def teacher_profile(request, user_id):
    teacher = get_object_or_404(Teacher, id=user_id)

    return render(request, 'users/teachers/teachers.html',
                  {'teacher': teacher})

#

