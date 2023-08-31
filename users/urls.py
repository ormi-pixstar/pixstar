from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 회원가입
    path('signup/', views.SignupView.as_view(), name='Signup'),
    # 로그인
    path('login/', views.LoginView.as_view(), name='Login'),
    # 로그아웃
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    # 회원탈퇴
    path('signout/', views.SignoutView.as_view(), name='signout'),
    # 회원정보 조회
    path('profile/', views.UserDetailView.as_view(), name='UserDetail'),
    # 회원정보 수정
    path('update/', views.UserUpdateView.as_view(), name='update'),
]
