from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
	title = models.CharField(max_length=255)
	content = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	resource_name = models.CharField(max_length=255, null=True)
	resource_url = models.CharField(max_length=255, null=True)
	
	def __str__(self):
		return self.title