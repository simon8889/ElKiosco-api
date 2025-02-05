from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListAllPosts.as_view(), name='all'),
    path('user/', views.UserPosts.as_view(), name='userposts'),
]