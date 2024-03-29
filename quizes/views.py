import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from courses.models import Module
from .forms import QuizForm, QuestionForm, question_formset
from .models import Quiz, Question, QuizResults
from courses.utils import is_teacher

# Create your views here.

@login_required
@user_passes_test(is_teacher)
def create_edit_quiz(request, module_id, quiz_id=None):
    module = get_object_or_404(Module, id=module_id)
    quiz_instance = None

    if quiz_id is not None:
        quiz_instance = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz_instance)
        formset = question_formset(request.POST, instance=quiz_instance)
        if quiz_form.is_valid() and formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.module = module
            quiz.course = module.course
            quiz.save()
            formset = formset.save(commit=False)
            for form in formset:
                form.quiz = quiz
                form.save()
            messages.success(request, 'Quiz created successfully')
        else:
            messages.info(request, 'There was a problem creating this quiz')

        return redirect('module_detail', slug=module.course.slug, module_id=module.id)
    else:
        quiz_form = QuizForm(instance=quiz_instance)
        formset = question_formset(instance=quiz_instance)

    return render(request, 'quizes/create_edit.html',
                  {'quiz_form': quiz_form,
                   'formset': formset, 'module': module})

@login_required
def start_quiz(request, quiz_id, classroom_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, 'quizes/quiz.html',
                  {'quiz': quiz,
                   "classroom_id": classroom_id})


@require_POST
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@require_POST
def finish_test(request, quiz_id):
    try:
        data = json.loads(request.body)
        questions = []
        score = 0
        quiz = get_object_or_404(Quiz, id=quiz_id)

        for i in data['questions']:
            question = Question.objects.get(question=i['question'].split('?')[0])
            questions.append({
                'question': question.question,
                'answer': i['answerText'],
                'correct': i['answer'] == question.correct_answer
            })

            if i['answer'] == question.correct_answer:
                score += 1
        response_data = {
            'status': 'ok',
            'final_results': questions,
            'score': 100 / 10 * score,
            'final_quiz': quiz.final,
        }
        if quiz.final:
            graduation_url = reverse("classroom:graduation", args=[quiz.course.id, data['classroom_id']])
            response_data["graduation_url"] = graduation_url

        QuizResults.objects.create(
            student=request.user.student_profile,
            quiz=quiz,
            result=score,
            passed= score > 50
        )

        return JsonResponse(response_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Return an error response
        return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)
