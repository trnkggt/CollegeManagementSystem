from django import forms
from django.forms.models import inlineformset_factory

from .models import Question, Quiz
from courses.models import Module

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('module', 'course')

    open_date = forms.DateTimeField(
        error_messages={'required': 'Open date for quiz is necessary'},
        widget=forms.DateTimeInput(
            attrs={
                'id': 'open-date'
            }
        )
    )
    close_date = forms.DateTimeField(
        error_messages={'required': 'Close date for quiz is necessary'},
        widget=forms.DateTimeInput(
            attrs={
                'id': 'close-date'
            }
        )
    )


question_formset = inlineformset_factory(
    Quiz, Question, form=QuestionForm,
    extra=10, can_delete=True, can_delete_extra=True, max_num=10
)