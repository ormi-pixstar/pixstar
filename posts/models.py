from django.db import models
from django.conf import settings


class Post(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images/')


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
