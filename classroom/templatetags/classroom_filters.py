from django import template
from quizes.models import QuizResults

register = template.Library()

@register.filter
def eligible_for_quiz(quiz, student_id):
    return QuizResults.objects.filter(student=student_id, quiz=quiz).exists()