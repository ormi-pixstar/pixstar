from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Post
        fields = ('id', 'content', 'created_at', 'updated_at', 'writer', 'likes_count')
