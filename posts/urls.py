from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPosts.as_view(), name='userposts'),
    path('all/', views.ListAllPosts.as_view(), name='all'),
    path('<int:post_id>/', views.UserPosts.as_view(), name='userpost-detail'),
    path('comments/<int:post_id>/', views.CommentsView.as_view(), name='posts_comments'),
    path('comments/modify/<int:comment_id>/', views.CommentsView.as_view(), name='comments')
]