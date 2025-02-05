from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

@api_view(["POST"])
def login(request):
	user = get_object_or_404(User, username=request.data["username"])
	
	if not user.check_password(request.data["password"]):
		return Response({"Error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
	
	token, created = Token.objects.get_or_create(user=user)
	serializer = UserSerializer(instance=user)
	return Response({"token": token.key, "user_id": serializer.data["id"]}, status=status.HTTP_200_OK)

@api_view(["POST"])
def register(request):
	serializer = UserSerializer(data=request.data)
	
	if serializer.is_valid():
		serializer.save()
		
		new_user = User.objects.get(username=serializer.data["username"])
		new_user.set_password(serializer.data["password"])
		new_user.save()
		
		token = Token.objects.create(user=new_user)
		return Response({"token": token.key, "user_id": serializer.data["id"]}, status=status.HTTP_201_CREATED)

	
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
	serializer = UserSerializer(instance=request.user)
	return Response({"user_id": serializer.data["id"], "username": serializer.data["username"]}, status=status.HTTP_200_OK)

