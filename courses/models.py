from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string



class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Course(models.Model):
    owner    = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)    
    subject  = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title    = models.CharField(max_length=200)
    slug     = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class Module(models.Model):
    course      = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order       = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)
    

class Content(models.Model):
    module       = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, 
                                                  limit_choices_to={'model__in':(
                                                                                 'text',
                                                                                 'image',
                                                                                 'file',
                                                                                 'video')})
    object_id    = models.PositiveIntegerField()
    item         = GenericForeignKey('content_type', 'object_id')
    order        = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title   = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name),
                                {'item': self})
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    body = models.TextField()

class Image(ItemBase):
    image = models.ImageField(upload_to='images/')

class Video(ItemBase):
    url = models.URLField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

