from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like_post', null=True, blank=True)


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images/', null=False, blank=False)
