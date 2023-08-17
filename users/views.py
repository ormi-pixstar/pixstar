from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm

# Create your views here.

class Index(View):
    def get(self, repuest):
        context = {
            "title" : "UserIndex"
        }
        return render(repuest, 'users/index.html', context)

### Signin
class Signin(View):
    def get(self, request):
        pass
    def post(self, request):
        pass



### Signout
class Signout(View):
    def get(self, request):
        pass
    def post(self, request):
        pass



### Login
class Login(View):
    def get(self, request):
        pass
    def post(self, request):
        pass



### Logout
class Logout(View):
    def get(self, request):
        pass
    def post(self, request):
        pass



### profile
class Profile(View):
    def get(self, request):
        pass
    def post(self, request):
        pass



### update
class Update(View):
    def get(self, request):
        pass
    def post(self, request):
        pass
