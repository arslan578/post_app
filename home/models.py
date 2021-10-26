from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Post(models.Model):
    post = models.TextField()
    like_count = models.BigIntegerField(default=0)
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
