from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    users = models.ManyToManyField(User, related_name='my_groups')
    name = models.CharField(max_length=150)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_group', blank=True, null=True)

class GroupMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='group_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class GroupPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)