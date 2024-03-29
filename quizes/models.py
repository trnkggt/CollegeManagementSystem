from django.db import models

# Create your models here.


class Quiz(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='quizes')
    module = models.OneToOneField('courses.Module', on_delete=models.CASCADE,
                               related_name='quiz')
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    active = models.BooleanField(default=False)
    open_date = models.DateTimeField(default=None)
    close_date = models.DateTimeField(default=None)
    final = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.module}'s {self.title} quiz"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=250)
    choice_a = models.CharField(max_length=150)
    choice_b = models.CharField(max_length=150)
    choice_c = models.CharField(max_length=150)
    choice_d = models.CharField(max_length=150)

    answer_choices = [
        ('A', 'Choice A'),
        ('B', 'Choice B'),
        ('C', 'Choice C'),
        ('D', 'Choice D')
    ]

    correct_answer = models.CharField(
        choices=answer_choices,
        max_length=1,
        verbose_name='correct_answer'
    )

    def __str__(self):
        return self.question


class QuizResults(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.SET_NULL, null=True,
                                related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    result = models.IntegerField()
    passed = models.BooleanField(default=False)
