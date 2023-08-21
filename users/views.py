from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import responses
from rest_framework import status
from .models import Profile
from .forms import SigninForm, LoginForm
from .serializers import ProfileSerializer

# Create your views here.

class Index(View):
    def get(self, request):
        context = {
            "title" : "UserIndex"
        }
        return render(request, 'users/index.html', context)

### Signin
class Signin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:logincheck')
        form = SigninForm()
        context = {
            "form" : form,
            "title" : "UserSignin"
        }
        return render(request, 'users/signin.html', context)
    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
        context = {
            'form' : form
        }
        return render(request, 'users/signin.html', context)



### Signout
class Signout(View):
    def get(self, request):
        context = {
            "title" : "UserSignout"
        }
        return render(request, 'users/signout.html', context)
    def post(self, request):
        pass



### Login
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:logincheck')
        
        form = LoginForm()
        context = {
            "form" : form,
            "title" : "UserLogin"
        }
        return render(request, 'users/login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('users:logincheck')
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('users:logincheck')
            
        form.add_error(None, '아이디가 없습니다.')
        
        context = {
            "form" : form
        }
        return render(request, 'users/login.html', context)



### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')



### profile
class Profile(APIView):
    # def get(self, request):
    #     context = {
    #         "title" : "UserProfile"
    #     }
    #     return render(request, 'users/profile.html', context)
    def post(self, request):
        user = request.data.get('user')

        profile = Profile.objects.create(user=user)
        serializer = ProfileSerializer(profile)

        return responses(serializer.data, status=status.HTTP_201_CREATED)



### update
class Update(View):
    def get(self, request):
        context = {
            "title" : "UserUpdate"
        }
        return render(request, 'users/update.html', context)
    def post(self, request):
        pass


### tempClass
class CheckFuntion(View):
    def get(self, request):
        context = {
            "title" : "FuntionCheck"
        }
        return render(request, 'users/logincheck.html', context)
    def post(self, request):
        pass
