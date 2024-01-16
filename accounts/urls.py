from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.register, name='register'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('logout/', views.LogoutView.as_view(), name='user_logout'),
    # path('profile/', views.profile, name='profile'),
]