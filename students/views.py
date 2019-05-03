from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import CourseEnrollForm
from courses.models import Course

class StudentRegisterationView(CreateView):
    template_name = 'students/student/registeration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            cd = form.cleaned_data
            user = authenticate(self.request, username=cd['username'], password=cd['password1'])
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())        
            
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    template_name = None
    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

class StudentCourseListView(LoginRequiredMixin, ListView):
    template_name = 'students/course/list.html'
    def get_queryset(self):
        return Course.objects.filter(students__in=[self.request.user])
   
class StudentCourseDetialView(DetailView):
    template_name = 'students/course/detail.html'
    model = Course
    def get_queryset(self):
        qs = super().get_queryset()
    
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.first()

        return context