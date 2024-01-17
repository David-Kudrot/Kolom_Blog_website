from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('contact/', views.ContactView.as_view(), name='contact_us'),

]