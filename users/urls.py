from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 회원가입
    path('signup/', views.Signup.as_view(), name='Signup'),
    # 회원탈퇴
    path('signout/', views.Signout.as_view(), name='signout'),
    # 로그인
    path('login/', views.Login.as_view(), name='Login'),
    # 로그아웃
    path('logout/', views.Logout.as_view(), name='Logout'),
    # 회원정보 조회
    path('profile/', views.UserDetail.as_view(), name='UserDetail'),
    # 회원정보 수정
    path('update/', views.UserUpdate.as_view(), name='update'),
]
