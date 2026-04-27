from django.urls import path, include
from jobs import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('jobs.urls')),
]