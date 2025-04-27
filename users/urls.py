from django.contrib import admin
from django.urls import path, include
from users import views
urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile'),
    path('<str:username>/edit/', views.edit_profile_view, name='edit'),
]