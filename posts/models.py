from django.db import models
from django.conf import settings


class Post(models.Model):
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images/', null=False, blank=False)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # 유저와 포스트의 유일성을 강제 -> 에러 처리 필요
    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='recomments', on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content