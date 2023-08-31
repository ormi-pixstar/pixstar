# Django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

# DjangoRestFramework
from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response

# DjangroRestFramework-simpleJWT
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

# Custom
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    SignoutSerializer,
    ProfileSerializer,
)
from .authentication import UserAuthenticationView, CookieJWTAuthentication


# 회원가입
class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Signup is successful'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class Login(APIView):
    message = '로그인 완료'
    status_code = status.HTTP_200_OK

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return UserAuthenticationView.set_token_cookies(self, user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### 로그아웃
class Logout(APIView):
    # def post(self, request):
    #     refresh_token = request.COOKIES.get('refresh')
    #     if refresh_token:
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()
    #     else:
    #         return Response('비정상적인 토큰입니다.', status=status.HTTP_400_BAD_REQUEST)
    #     response = Response('로그아웃 완료')
    #     response.set_cookie('refresh', httponly=True, samesite='None', secure=True)
    #     return response

    def post(self, request):
        response = Response({"message": "로그아웃"}, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


# 회원탈퇴
class Signout(APIView):
    def post(self, request):
        user = request.user

        serializer = SignoutSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response("회원탈퇴되었습니다.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### 회원조회
class UserDetail(APIView):
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### 회원수정
class UserUpdate(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
