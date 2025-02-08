from django.urls import path, include
from . import views

post_patterns = [
    path('', views.UserPosts.as_view(), name='userposts'),
    path('all/', views.ListAllPosts.as_view(), name='allposts'),
    path('<int:post_id>/', views.UserPosts.as_view(), name='userpost-detail'),
]

comment_patterns = [
    path('<int:post_id>/', views.CommentsView.as_view(), name='posts_comments'),
    path('modify/<int:comment_id>/', views.CommentsView.as_view(), name='comments'),
]

vote_patterns = [
    path('post/<int:post_id>/', views.vote_post, name='votepost'),
    path('comment/<int:comment_id>/', views.vote_comment, name='votecomment'),
    path('remove/post/<int:post_id>/', views.remove_vote_post, name='votepost'),
    path('remove/comment/<int:comment_id>/', views.remove_vote_comment, name='votecomment'),
    path("change/post/<int:post_id>/", views.change_vote_type_post, name="changevotepost"),
    path("change/comment/<int:comment_id>/", views.change_vote_type_comment, name="changevotecomment"),
]

urlpatterns = [
    path('posts/', include((post_patterns, 'posts'))),
    path('comments/', include((comment_patterns, 'comments'))),
    path('votes/', include((vote_patterns, 'votes'))),
]