from django.contrib import admin
from django.urls import path, include
from platforms import views
urlpatterns = [
    path('codechef/', views.codechef, name='codechef'),
    path('codeforces/', views.codeforces, name='codeforces'),
    path('refresh/', views.refresh_potd_status, name='refresh_potd_status'),
    path('addproblems/', views.addproblems, name='addproblems'),
]