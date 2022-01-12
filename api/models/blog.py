from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from total_weather_backend import settings

User = settings.AUTH_USER_MODEL

class Blog(models.Model):
  image = models.ImageField(null=True, blank=True, upload_to="images/")
  title = models.CharField(max_length=100)
  author = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
  content = models.CharField(max_length=1000)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    # This must return a string
    return f"{self.image} - Created at: {self.created_at} by {self.author} - Updated at: {self.updated_at} - Title: {self.title} - Content: {self.content}"
