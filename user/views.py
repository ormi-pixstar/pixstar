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
from .serializers import UserSerializer
