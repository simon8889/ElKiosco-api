from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
	title = models.CharField(max_length=255)
	content = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	resource_name = models.CharField(max_length=255, null=True)
	resource = models.FileField(upload_to="media/", null=True)
	tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  
	parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comment by {self.author} on {self.post}"
	
class Vote(models.Model):
	class VoteType(models.TextChoices):
		UPVOTE = "UP", "Upvote"
		DOWNVOTE = "DOWN", "Downvote"
	
	voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")  
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="votes")
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="votes")
	vote_type = models.CharField(max_length=4, choices=VoteType.choices)
	
	def __str__(self):
		return f"{self.voter} voted {self.get_type_display()} on {self.post}"
	
