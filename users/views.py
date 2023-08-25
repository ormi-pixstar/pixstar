# Django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

# DjangoRestFramework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Custom
from .models import *
from .forms import *
from .serializers import *

# Create your views here.

### 회원가입
class Signin(APIView):
    def post(self, request):
        serializer = SigninSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("회원가입에 성공했습니다.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


### 회원탈퇴
class Signout(APIView):
    def post(self, request):
        user = request.user

        serializer = SignoutSerializer(data=request.data, context={"user":user})
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response("회원탈퇴되었습니다.")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


### 로그인
class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            response = Response(
                {
                    "user" : { "id" : user.pk, "name" : user.name },
                    "message" : "로그인 완료"
                },
                status = status.HTTP_200_OK
            )
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



### 로그아웃
class Logout(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass



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
