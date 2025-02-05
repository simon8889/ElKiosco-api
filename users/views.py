from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer

@api_view(["POST"])
def login(request):
	serializer = LoginSerializer(data=request.data)
	if not serializer.is_valid():
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	user = serializer.validated_data
	token, created = Token.objects.get_or_create(user=user)
	user_serializer = UserSerializer(instance=user)
	return Response({"token": token.key, "user_id": user_serializer.data["id"]}, status=status.HTTP_200_OK)
	
@api_view(["POST"])
def register(request):
	serializer = UserSerializer(data=request.data)
	if not serializer.is_valid():
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	user = serializer.save()
	token = Token.objects.create(user=user)
	return Response({"token": token.key, "user_id": user.id}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
	serializer = UserSerializer(instance=request.user)
	return Response({"user_id": serializer.data["id"], "username": serializer.data["username"]}, status=status.HTTP_200_OK)