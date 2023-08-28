from rest_framework import serializers
from .models import Post, Image, Comment


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

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        images_data = self.context['request'].FILES

        if 'images' not in images_data:
            images_data = None

        if images_data is not None:
            images = Image.objects.filter(post=instance)
            images.delete()
            for image_data in images_data.getlist('images'):
                Image.objects.create(post=instance, image=image_data)
        instance.save()
        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    like = serializers.StringRelatedField(many=True)
    like_count = serializers.IntegerField(source='like.count')

    class Meta:
        model = Post
        fields = ["like", "like_count"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comments",)
