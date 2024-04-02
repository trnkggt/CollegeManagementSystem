from django import forms
from django.utils import timezone


from .models import Classroom
from users.models import StudentProfile, Teacher
from courses.models import Subject

class ClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = '__all__'
        exclude = ['course', ]

    title = forms.CharField(
        error_messages={'required': 'title is Required'},
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control form-control-lg',
            }
        ))
    student_count = forms.IntegerField(
        error_messages={'required': 'Student count is required',
                        'IntegrityError': 'Provide valid number'},
        widget=forms.NumberInput(
            attrs={
                'type': 'number',
                'class': 'form-control form-control-lg',
            }
        ))
    active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                'class': 'form-control form-check-input',
                'label': 'Active'
            }
        ),
        required=False
    )
    start_date = forms.DateTimeField(
        error_messages={'required': 'Start date for classroom is necessary'},
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'start-date'
            }
        )
    )
    end_date = forms.DateTimeField(
        error_messages={'required': 'Ending date for classroom is necessary'},
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'end-date'
            }
        )
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        error_messages={'required': 'Classroom should have a teacher'},
        widget=forms.Select(
            attrs={
                'id': 'teacher',
                'class': 'form-select '

            }
        ),
        required=True
    )
    subject = forms.CharField(
        error_messages={'required': 'Classroom should have a main subject'},
        widget=forms.Select(
            attrs={
                'id': 'subjects',
                'class': 'form-select'
            }
        )
    )
    students = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.filter(enrolled=False),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
                'placeholder': 'Teacher',
            }
        ),
        required=False
    )

    def clean_student_count(self):
        data = self.cleaned_data
        count = data['student_count']
        if count < 1:
            raise forms.ValidationError(message='Please provide valid number,'
                                                ' it should be more than 0')
        return count


    def clean_end_date(self):
        data = self.cleaned_data
        end = data['end_date']
        today = timezone.now()
        diff = end - today
        if diff.days < 1:
            raise forms.ValidationError(message='Please provide valid ending date')
        return end

    def clean_subject(self):
        data = self.cleaned_data

        return Subject.objects.get(id=int(data['subject']))
