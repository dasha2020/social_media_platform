from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    admin_in_group = models.BooleanField(default=False)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    photo = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def top_level_comments(self):
        return self.comments.filter(comment_of_reply__isnull=True)\
                   .prefetch_related('replies')\
                   .order_by('-created_at')

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True) # user, who clicked follow 
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True) # user, who gets a new follower

#class Notification(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    #like = models.ForeignKey(Like, on_delete=models.SET_NULL, null=True)






