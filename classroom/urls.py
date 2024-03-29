from django.urls import path

from . import views


app_name = 'classroom'
urlpatterns = [
    path('create/', views.create_edit_classroom, name='classroom_create'),
    path('edit/<int:classroom_id>',
         views.create_edit_classroom, name='classroom_update'),
    path('classrooms/all/', views.classroom_list, name='classroom_list'),

    #Teacher
    path('classrooms/mine/', views.teacher_classroom, name='teachers_classroom'),
    path('classrooms/mine/<int:classroom_id>/',
         views.classroom_details, name='classroom_details'),

    path('classrooms/mine/<int:classroom_id>/teacher/courses',
         views.get_teacher_course_list, name='teacher-courses'),
    path('classrooms/mine/enroll/<int:classroom_id>/',
         views.enroll_classroom,
         name='enroll-classroom'),

    #Student
    path('classrooms/detail/<int:classroom_id>/',
         views.classroom_details_students,
         name='classroom_detail_students'),
    path('classrooms/detail/<int:classroom_id>/enroll/',
         views.enroll_student,
         name='enroll_student'),
    path('classrooms/<int:classroom_id>/detail/module/<int:module_id>/content',
         views.classroom_modules,
         name='student_classroom_module'),
    path('classrooms/student/results/',
         views.student_results,
         name='student_results'),
    path('graduation/<int:course_id>/<int:classroom_id>/',
         views.graduate_student,
         name='graduation')
]