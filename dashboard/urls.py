from django.urls import path

from . import views

app_name='dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('classes/all/', views.admin_dashboard_classes, name='classroom_list'),
    path('teachers/all/', views.teacher_list, name='teacher_list'),
    path('students/all/', views.student_list, name='student_list'),

    path('teachers/<subject>/', views.teacher_list, name='teachers_subject'),
    path('teachers/classrooms/<int:teacher_id>/', views.teacher_classrooms, name='teachers_classrooms'),
]