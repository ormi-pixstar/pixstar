from rest_framework import serializers
from .models import Post, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["images", "content", "writer", "created_at", "updated_at"]

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(post=post, image=image)
        return post


class PostLikeSerializer(serializers.ModelSerializer):
    like = serializers.StringRelatedField(many=True)
    like_count = serializers.IntegerField(source='like.count')

    class Meta:
        model = Post
        fields = ["like", "like_count"]