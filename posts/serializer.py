from rest_framework import serializers
from .models import Post

class PostsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "resource_name", "resource_url"]
