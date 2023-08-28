from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignoutSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'profile_img']
