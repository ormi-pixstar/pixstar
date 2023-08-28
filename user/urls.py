from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 회원가입
    path('signup/', views.SignupView.as_view(), name='signup'),
    # 로그인
    path('login/', views.LoginView.as_view(), name='login'),
    # 로그아웃
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 회원탈퇴
    # path('sginout/', views.Signout.as_view(), name='signout'),
    # # 회원정보 조회
    # path('profile/', views.UserDetail.as_view(), name='UserDetail'),
    # # 회원정보 수정
    # path('update/', views.UserUpdate.as_view(), name='update'),
]
