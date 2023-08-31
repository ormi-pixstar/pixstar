from rest_framework import serializers
from .models import Post, Image, Comment
from .S3Storage import S3Storage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image_url"]


class PostSerializer(serializers.ModelSerializer):
    image_urls = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["image_urls", "content"]

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        images_data = self.context['request'].FILES
        s = S3Storage()
        for image in images_data.getlist('images'):
            s.upload(post.pk, image)
            Image.objects.create(post=post, image_url=s.getUrl())
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        images_data = self.context['request'].FILES

        if 'images' not in images_data:
            images_data = None

        if images_data is not None:
            s = S3Storage()
            images = Image.objects.filter(post=instance)
            for image in images:
                s.delete(image)
            images.delete()
            for image_data in images_data.getlist('images'):
                s.upload(instance.pk, image_data)
                Image.objects.create(post=instance, image_url=s.getUrl())
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
