from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('listings/', views.home, name='home'),
    path('contact/', views.home, name='home'),
    path('buy/', views.home, name='home'),
    path('rent/', views.home, name='home'),
    path('sell/', views.home, name='home'),
]
