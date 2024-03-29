from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import F
from django.template.loader import render_to_string
from django.conf import settings

from .fields import CustomPositiveIntegerField

# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['title',]

    def __str__(self):
        return self.title


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name='courses',
                                on_delete=models.CASCADE)
    # When teacher account may be deleted FK will be set to null
    # So that admin can assign different teacher
    teacher = models.ForeignKey('users.Teacher', related_name='courses_taught',
                                on_delete=models.SET_NULL,
                                null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    overview = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=10, null=True, unique=True)
    credits = models.IntegerField(null=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False,
                                           blank=True)
    price = models.DecimalField(default=15, null=True,
                                decimal_places=2, max_digits=6)


    def __str__(self):
        return f'{self.title}'


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)
    description = models.TextField(max_length=500)
    order = CustomPositiveIntegerField(null=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        after_objs = Module.objects.filter(order__gt=self.order).update(order=F('order')-1)

        return super().delete(using=None, keep_parents=False)

class Content(models.Model):
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='contents')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id',)
    order = CustomPositiveIntegerField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

    def delete(self, using=None, keep_parents=False):
        Content.objects.filter(order__gt=self.order).update(order=F('order')-1)

        super().delete(using=None, keep_parents=False)

class ItemBase(models.Model):
    teacher = models.ForeignKey('users.Teacher',
                                related_name='%(class)s_related',
                                on_delete=models.SET_NULL,
                                null=True)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'classroom/module/content/{self._meta.model_name}.html',
            {"item": self,
             "MEDIA_URL": settings.MEDIA_URL}
        )


class Text(ItemBase):
    content = models.TextField()
    content_relation = GenericRelation('Content')

class File(ItemBase):
    file = models.FileField(upload_to='files/contents')
    content_relation = GenericRelation('Content')


class Video(ItemBase):
    url = models.URLField()
    content_relation = GenericRelation('Content')

class Image(ItemBase):
    image = models.ImageField(upload_to='images/contents')
    content_relation = GenericRelation('Content')
