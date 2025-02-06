from rest_framework import serializers
from .models import Post, Tag, Comment, Vote

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "resource_name", "resource_url", "tags"]
       
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
        return post
     
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context.get("request").user
        data["upvote_count"] = Vote.objects.filter(post_id=data["id"], vote_type="UP").count()
        data["downvote_count"] = Vote.objects.filter(post_id=data["id"], vote_type="DOWN").count()
        user_has_vote = Vote.objects.filter(voter=user.id, post_id=data["id"]).first()
        data["user_has_voted"] = user_has_vote.vote_type if user_has_vote else None
        return data

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta: 
        model = Comment
        fields = ["id", "author", "post", "content", "created_at", "parent"]

class VotesSerializer(serializers.ModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Vote
        fields = ["id", "voter", "post", "comment", "vote_type"]