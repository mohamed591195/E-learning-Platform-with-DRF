from django import forms
from .models import Content, Module, Course
from django.forms.models import inlineformset_factory

ModuleFormset = inlineformset_factory(Course, 
                                      Module, 
                                      fields=['title', 'description'], 
                                      extra=2, 
                                      can_delete=True)
