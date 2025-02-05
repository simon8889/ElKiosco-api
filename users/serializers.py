from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "password"]
	
	def create(self, validated_data):
		user = User(
			username=validated_data["username"]
		)
		user.set_password(validated_data["password"])  
		user.save()
		return user

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150)
	password = serializers.CharField(write_only=True)
	
	def validate(self, data):
		user = authenticate(username=data["username"], password=data["password"])
		if not user:
			raise serializers.ValidationError("Invalid username or password")
		return user
	