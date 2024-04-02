from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.utils import timezone
from django_countries.widgets import CountrySelectWidget
from django_countries import countries

import re
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import CustomUser, StudentProfile, Teacher
from .tasks import sent_from_admin

class NewUserForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    USER_TYPES = (
        ('', 'Choose account type'),
        ('S', 'Student'),
        ('T', 'Teacher')
    )
    first_name = forms.CharField(
        error_messages={'required': 'First name is Required'},
        widget=forms.TextInput(attrs={'type': 'text',
                                      'class': 'form-control form-control-lg',
                                      'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        error_messages={'required': 'Last name is Required'},
        widget=forms.TextInput(attrs={'type': 'text',
                                      'class': 'form-control form-control-lg',
                                      'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is Required'},
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control form-control-lg',
            'placeholder': 'Email'
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control form-control-lg',
            'placeholder': 'Password'
        }
    ),
        error_messages={'required': 'Password is Required'},
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control form-control-lg',
            'placeholder': 'Repeat Password'
        }
    ),
        error_messages={'required': 'Password is Required'},
    )
    address = forms.CharField(
        error_messages={'required': 'Address is Required'},
        widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control form-control-lg',
            'placeholder': 'Address'
        }
    ))
    gender = forms.ChoiceField(
        error_messages={'required': 'Gender is Required'},
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg',
               'placeholder': 'Gender'}
    ))
    date_of_birth = forms.DateField(
        error_messages={'required': 'Birth date is Required'},
        widget=DatePickerInput(
            attrs={'class': 'form-control form-control-lg',
                   'placeholder': 'Birth date'}))

    country = forms.ChoiceField(
        error_messages={'required': 'Country of origin is Required'},
        choices=countries,
        widget=CountrySelectWidget(
            attrs={'class': 'form-select form-select-lg',
                   'placeholder': 'Birth date'}
        )
    )
    user_type = forms.ChoiceField(label='Account type',
                                  choices=USER_TYPES,
                                  widget=forms.Select(
                                      attrs={
                                          'class': 'form-select form-select-lg d-inline-block'}
                                  ))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1',
                  'password2', 'date_of_birth', 'address', 'gender',
                  'country')
        # widgets = {'country': CountrySelectWidget(attrs={'class': 'form-control form-control-lg',
        #            })}


    def clean_date_of_birth(self):
        """
        Clean date field to check if user is at least 18yo.
        """
        date = self.cleaned_data['date_of_birth']
        current_date = timezone.now().date()
        diff = current_date - date
        if diff.days >= 18*365:
            return date
        else:
            raise forms.ValidationError('You should be at least 18 years old')

    def clean_first_name(self):
        """
        Clean username so that it only contains characters
        """
        first_name = self.cleaned_data['first_name']
        if not re.match("^[a-zA-Z]*$", first_name):
            raise forms.ValidationError('First name should only contain characters')
        else:
            return first_name
    def clean_last_name(self):
        """
        Clean last name so that it only contains characters
        """
        last_name = self.cleaned_data['last_name']
        if not re.match("^[a-zA-Z]*$", last_name):
            raise forms.ValidationError('Last name should only contain characters')
        else:
            return last_name
class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True,
                                                               'class': 'form-control'}))

# Student/Teacher profile forms
class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_picture']
        widgets = {'profile_picture': forms.FileInput(
            attrs={'class': 'form-control form-control-lg d-inline-block'})}

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['about', 'experience', 'education', 'profile_picture']
        widgets = {
            'about': forms.Textarea(
            attrs={'class': 'form-control form-control-sm'}
            ),
            'experience': forms.Textarea(
                attrs={'class': 'form-control form-control-sm'},
            ),
            'education': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'profile_picture': forms.FileInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'about': 'About me',
            'experience': 'My work experience',
            'education': 'Formal education',
        }
#

class UserAdminUpdateForm(UserChangeForm):
    email_subject = forms.CharField(required=False)
    email_body = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean(self):
        email_subject = self.cleaned_data['email_subject']
        email_body = self.cleaned_data['email_body']
        to_email = self.cleaned_data['email']
        if email_subject != '' and email_body != '':
            sent_from_admin.delay(email_subject, email_body, to_email)
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'date_of_birth', 'address', 'gender',
                  'country')

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = forms.CharField(
        error_messages={'required': 'First name is Required'},
        widget=forms.TextInput(attrs={'type': 'text',
                                      'class': 'form-control form-control-lg',
                                      'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        error_messages={'required': 'Last name is Required'},
        widget=forms.TextInput(attrs={'type': 'text',
                                      'class': 'form-control form-control-lg',
                                      'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is Required'},
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control form-control-lg',
            'placeholder': 'Email'
        }))
    address = forms.CharField(
        error_messages={'required': 'Address is Required'},
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control form-control-lg',
                'placeholder': 'Address'
            }
        ))
    gender = forms.ChoiceField(
        error_messages={'required': 'Gender is Required'},
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg',
                                   'placeholder': 'Gender'}
                            ))
    date_of_birth = forms.DateField(
        error_messages={'required': 'Birth date is Required'},
        widget=DatePickerInput(
            attrs={'class': 'form-control form-control-lg d-inline-block',
                   'placeholder': 'Birth date'}))

    country = forms.ChoiceField(
        error_messages={'required': 'Country of origin is Required'},
        choices=countries,
        widget=CountrySelectWidget(
            attrs={'class': 'form-select form-select-lg d-inline-block',
                   'placeholder': 'Birth date'}
        )
    )