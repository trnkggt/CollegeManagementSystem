from django.db import models

# Create your models here.
class ClassroomManager(models.Manager):
    def get_queryset(self):
        return super(ClassroomManager, self).get_queryset().filter()


class Classroom(models.Model):
    title = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL,
                               null=True, related_name='classrooms')
    student_count = models.PositiveIntegerField()
    teacher = models.ForeignKey('users.Teacher', related_name='classrooms',
                                on_delete=models.SET_NULL,
                                null=True)
    subject = models.ForeignKey('courses.Subject', on_delete=models.SET_NULL,
                               null=True, related_name='classrooms')
    students = models.ManyToManyField('users.StudentProfile',
                                      related_name='joined_class')
    active = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def __str__(self):
        return self.title


