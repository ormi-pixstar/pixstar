from rest_framework import serializers
from .models import Post, Image, Comment
from .storage import S3Storage
from user.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image_url"]


class PostLikeSerializer(serializers.ModelSerializer):
    like = serializers.StringRelatedField(many=True)
    like_count = serializers.IntegerField(source="like.count")

    class Meta:
        model = Post
        fields = ["like", "like_count"]


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="user.writer")
    post_id = serializers.ReadOnlyField(source="post.pk")
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "post_id",
            "id",
            "writer",
            "parent",
            "comment",
            "created_at",
            "updated_at",
            "reply",
        ]

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind("", self)
        return serializer.data


class PostDetailSerializer(serializers.ModelSerializer):
    image_urls = ImageSerializer(many=True, read_only=True)
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    image_urls = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["image_urls", "content"]
    
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        images_data = self.context['request'].FILES
        s = S3Storage()
        for image in images_data.getlist('image_urls'):
            s.upload(post.pk, image)
            Image.objects.create(post=post, image_url=s.getUrl())
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        images_data = self.context["request"].FILES

        if "image_urls" not in images_data:
            images_data = None

        if images_data is not None:
            s = S3Storage()
            images = Image.objects.filter(post=instance)
            
            for image in images:
                s.delete(image)
            images.delete()
            
            for image_data in images_data.getlist('image_urls'):
                s.upload(instance.pk, image_data)
                Image.objects.create(post=instance, image_url=s.getUrl)

        instance.save()
        return instance