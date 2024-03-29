from django.urls import path

from . import views


urlpatterns = [
    path('mine/', views.teacher_courses, name='teacher_courses'),

    path('all/', views.course_list, name='course_list'),

    path('ajax/courses/', views.subject_list_ajax, name='subject_list_ajax'),

    path('create/course/', views.create_or_update_course, name='course_create'),
    path('edit/course/<int:course_id>/', views.create_or_update_course,
         name='course_update'),
    path('detail/<int:pk>/', views.course_detail, name='course_detail'),

    path('course/<slug:slug>/<int:module_id>/', views.module_detail,
         name='module_detail'),
    path('course/<int:course_id>/modules/update/', views.module_add_edit,
         name='module_update'),

    path('course/<int:module_id>/<model_name>/', views.content_create,
         name='content_create'),
    path('course/<int:module_id>/<model_name>/<int:id>/', views.content_create,
         name='content_update'),

    # Delete and reorder with JS
    path('course/module/content/delete/', views.delete_content,
         name='content_delete'),

    # for ordering JS
    path('course/<order_type>/order/', views.module_order,
         name='module_order'),

]