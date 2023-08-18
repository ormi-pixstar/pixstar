from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # user 기능 확인용 로그인 완료
    path('logincheck/', views.CheckFuntion.as_view(), name='logincheck'),
    # 회원가입
    path('signin/', views.Signin.as_view(), name='signin'),
    # 회원탈퇴
    path('signout/', views.Signout.as_view(), name='signout'),
    # 로그인
    path('login/', views.Login.as_view(), name='login'),
    # 로그아웃
    path('logout/', views.Logout.as_view(), name='logout'),
    # 회원정보 조회
    path('profile/', views.Profile.as_view(), name='profile'),
    # 회원정보 수정
    path('Update/', views.Update.as_view(), name='update'),
    
]