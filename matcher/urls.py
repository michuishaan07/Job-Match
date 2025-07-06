
from django.urls import path
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.job_summary, name='dashboard'),
    path('upload/', views.resume_upload, name='resume_upload'),
 
]