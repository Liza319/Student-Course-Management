from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll'),
    path('files/', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
]