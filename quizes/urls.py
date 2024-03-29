from django.urls import path

from .views import create_edit_quiz, start_quiz, finish_test, delete_quiz

app_name = 'quizes'

urlpatterns = [
    path('<int:module_id>/quiz/create/', create_edit_quiz, name='create'),
    path('<int:module_id>/quiz/edit/<int:quiz_id>/', create_edit_quiz, name='edit_quiz'),

    path('start/<int:quiz_id>/<int:classroom_id>/', start_quiz, name='quiz_start'),
    path('<int:quiz_id>/finish/quiz/', finish_test, name='finish_quiz'),
    path('delete/<int:quiz_id>/', delete_quiz, name='delete_quiz')
]
