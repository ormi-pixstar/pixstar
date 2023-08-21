from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image_data in images_data.getlist('images'):
            Image.objects.create(post=post, image=image_data)
        return post
    

# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ["user", "like"]


# class PostSerializer(serializers.ModelSerializer):
#     likes_count = serializers.IntegerField(read_only=True, default=0)

#     class Meta:
#         model = Post
#         fields = ('id', 'content', 'created_at', 'updated_at', 'writer', 'likes_count')
