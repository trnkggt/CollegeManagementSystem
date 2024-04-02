import os

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django_countries.fields import CountryField
from django_resized import ResizedImageField
from django.urls import reverse

from .managers import CustomUserManager
from courses.models import Subject

class CustomUser(AbstractUser, PermissionsMixin):
    """
    Remove username as primary identificator for user and add email instead
    also add few additional fields.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    USER_CHOICES = (
        ('S', 'Student'),
        ('T', 'Teacher')
    )
    username = None
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=150)
    gender = models.TextField(choices=GENDER_CHOICES, max_length=1, null=True)
    country = CountryField(null=True)
    user_type = models.CharField(choices=USER_CHOICES, null=True, max_length=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def account_type(self):
        return ('%s' % (self.user_type))

    account_type.short_description = 'Account Type'


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='student_profile')
    has_graduated = models.BooleanField(default=False, null=True)
    enrolled = models.BooleanField(default=False, null=True)
    classroom = models.ForeignKey("classroom.Classroom",
                                  on_delete=models.CASCADE,
                                  related_name="enrolled_students",
                                  null=True,
                                  blank=True)
    profile_picture = ResizedImageField(size=[150, 150],
                                        upload_to='images/student_profiles/',
                                        null=True)
    courses = models.ManyToManyField('courses.Course',
                                         through='CourseBuying',
                                     related_name='students_bought')

    courses_passed = models.ManyToManyField("courses.Course",
                                            through="CoursePassing",
                                            related_name="students_passed")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self.id:
            old_instance = StudentProfile.objects.get(id=self.id)

            if self.profile_picture != old_instance.profile_picture:
                if old_instance.profile_picture:
                    if os.path.isfile(old_instance.profile_picture.path):
                        os.remove(old_instance.profile_picture.path)
        super().save(*args, **kwargs)

class CoursePassing(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)
    score = models.PositiveIntegerField()


class CourseBuying(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='teacher_profile')
    about = models.TextField(blank=True)
    subjects_taught = models.ManyToManyField(Subject)
    profile_picture = ResizedImageField(size=[150, 150],
                                        upload_to='images/teacher_profiles/',
                                        blank=True)
    experience = models.TextField(blank=True, null=True)
    education = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    def save(self, *args, **kwargs):
        """
        check if user changed profile picture,
        if positive, delete old picture
        """
        if self.id:
            old_instance = Teacher.objects.get(id=self.id)

            if self.profile_picture != old_instance.profile_picture:
                if old_instance.profile_picture:
                    if os.path.isfile(old_instance.profile_picture.path):
                        os.remove(old_instance.profile_picture.path)
        super().save(*args, **kwargs)


