from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Vote
from .serializer import PostsSerializer, CommentsSerializer, VotesSerializer
from .services import vote_entity, remove_vote_entity

class ListAllPosts(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		posts = [PostsSerializer(instance=post).data for post in Post.objects.all()]
		return Response({"posts": posts}, status=status.HTTP_200_OK)

class UserPosts(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		posts = Post.objects.filter(author_id=request.user.id)
		serializer = PostsSerializer(posts, many=True, context={"request": request})
		return Response({"posts": serializer.data}, status=status.HTTP_200_OK)
	
	def post(self, request):
		serializer = PostsSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		serializer.save(author=request.user)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	def delete(self, request, post_id):
		post = get_object_or_404(Post, id=post_id, author=request.user)
		post.delete()
		return Response({"deleted": True}, status=status.HTTP_200_OK)

	def put(self, request, post_id):
		post = get_object_or_404(Post, id=post_id, author=request.user)
		serializer = PostsSerializer(post, data=request.data, partial=True)
		
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

class CommentsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	
	def get(self, request, post_id):
		get_object_or_404(Post, id=post_id)
		comments = [CommentsSerializer(instance=comment).data for comment in Comment.objects.filter(post_id=post_id)]
		return Response({"comments": comments}, status=status.HTTP_200_OK)
	
	def post(self, request, post_id):
		post = get_object_or_404(Post, id=post_id)
		serializer = CommentsSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		serializer.save(author=request.user, post=post)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	def delete(self, request, comment_id):
		comment = get_object_or_404(Comment, id=comment_id, author=request.user)
		comment.delete()
		return Response({"deleted": True}, status=status.HTTP_200_OK)
	
	def put(self, request, comment_id):
		comment = get_object_or_404(Comment, id=comment_id, author=request.user)
		serializer = CommentsSerializer(comment, data=request.data, partial=True)
		
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote_post(request, post_id):
    data, errors = vote_entity(request.user, Post, post_id, request.data)
    if errors:
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote_comment(request, comment_id):
    data, errors = vote_entity(request.user, Comment, comment_id, request.data)
    if errors:
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)
	
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_vote_post(request,  post_id):
    removed = remove_vote_entity(request.user, Post, post_id)
    return Response({"deleted": removed}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_vote_comment(request, comment_id):
    removed = remove_vote_entity(request.user, Comment, comment_id)
    return Response({"deleted": removed}, status=status.HTTP_200_OK)