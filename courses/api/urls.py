from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('courses', views.CourseViewSet)

app_name = 'courses'

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    # path('courses/<int:pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
    path('', include(router.urls))
    
]   