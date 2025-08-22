from django.db import models
from django.contrib.auth.models import User
from comment_like.models import Comment, Like
from social_media_app.models import Post

# Create your models here.

class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    like = models.ForeignKey(Like, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10)

