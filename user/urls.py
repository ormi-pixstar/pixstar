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
    path('signout/', views.SignoutView.as_view(), name='signout'),
    # 전체 프로필 조회
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    # 유저 프로필 수정
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
]
