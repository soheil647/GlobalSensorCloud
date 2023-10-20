from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
