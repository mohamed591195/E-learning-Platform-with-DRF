from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'courses'

urlpatterns = [
     path('login/', auth_views.LoginView.as_view(template_name='courses/auth/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='courses/auth/logout.html'), name='logout'),
     path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
     path('create/', views.CourseCreateView.as_view(), name='course_create'),
     path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
     path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
     path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
     path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
     path('module/<int:module_id>/content/<model_name>/<int:id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
     path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
     path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
     # path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
     # path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
     path('subject/<slug:subject_slug>/', views.CourseListView.as_view(), name='course_list_subject'), 
     path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]