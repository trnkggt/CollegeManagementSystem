from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)


from . import views

app_name = 'users'

urlpatterns = [
    # Auth links
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password-reset/',
         PasswordResetView.as_view(
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password-change/',
         PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done')),
         name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    # Profile
    path('student/edit/', views.student_edit_profile, name='student-profile-edit'),
    path('student/<int:user_id>/', views.student_profile, name='student-profile'),
    path('teacher/edit/', views.teacher_edit_profile, name='teacher-profile-edit'),
    path('teacher/<int:user_id>/', views.teacher_profile, name='teacher-profile'),

]