from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 회원가입
    path('signinAPI/', views.SigninAPI.as_view(), name='SigninAPI'),
    # 회원탈퇴
    path('sginoutAPI', views.SignoutAPI.as_view(), name='signoutAPI'),
    # 로그인
    path('loginAPI/', views.LoginAPI.as_view(), name='LoginAPI'),
    # 로그아웃
    path('logoutAPI/', views.LogoutAPI.as_view(), name='LogoutAPI'),
    # 회원정보 조회
    path('detailAPI/', views.UserDetailAPI.as_view(), name='UserDetailAPI'),
    # 회원정보 수정
    path('updateAPI/', views.UserUpdateAPI.as_view(), name='updateAPI'),
]