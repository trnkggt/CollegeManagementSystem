from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={"class": 'form-control-sm'})}

ModuleInLine = inlineformset_factory(Course, Module,
                                     form=ModuleForm,
                                     extra=2)


class CourseCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher')
        super(CourseCreateForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Course
        fields = ['title','overview', 'subject', 'credits', 'code',
                  'prerequisites', 'price']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'overview': forms.Textarea(
                       attrs={"class": 'form-control-sm'}),
                   'subject': forms.Select(attrs={'class': 'form-select'}),
                   'code': forms.TextInput(attrs={'class': 'form-control'}),
                   'credits': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'prerequisites': forms.SelectMultiple(attrs={'class': 'form-select'}
                                    )}



    def clean_subject(self):
        data = self.cleaned_data
        teacher = self.teacher
        if not data['subject'] in teacher.subjects_taught.all():
            raise forms.ValidationError('You are not allowed to create course '
                                        'for this subject')
        else:
            return data['subject']

