from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Post


class ListAllPosts(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		posts = [post for post in Post.objects.all()]
		return Response(posts, status=status.HTTP_200_OK)

class UserPosts(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		posts = [post for post in Post.objects.filter(author_id=request.user.id)]
		return Response(posts, status=status.HTTP_200_OK)
	