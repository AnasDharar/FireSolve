from django.contrib import admin
from django.urls import path, include
from accounts import views
urlpatterns = [
    path('signup/', view = views.signup, name = 'signup'),
    path('login/', view = views.loginUser, name = 'login'),
    path('logout/', view = views.logoutUser, name = 'logout')
]