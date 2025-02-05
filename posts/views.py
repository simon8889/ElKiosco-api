from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializer import PostsSerializer

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
		posts = [PostsSerializer(instance=post).data for post in Post.objects.filter(author_id=request.user.id)]
		return Response({"posts": posts}, status=status.HTTP_200_OK)
	
	def post(self, request):
		serializer = PostsSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		serializer.save(author=request.user)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	def delete(self, request, post_id):
		post = get_object_or_404(Post, id=post_id, author=request.user)
		post.delete()
		return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)

	def put(self, request, post_id):
		post = get_object_or_404(Post, id=post_id, author=request.user)
		serializer = PostsSerializer(post, data=request.data, partial=True)
		
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
		
	
		
		
	