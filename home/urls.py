from django.contrib import admin
from django.urls import path, include
from home import views
from accounts import views as accounts_views
urlpatterns = [
    path('',view=views.landing, name = 'landing'),
    path('dashboard/',view=views.dashboard, name = 'dashboard'),
    
]