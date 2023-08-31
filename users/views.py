# DjangoRestFramework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

# DjangroRestFramework-simpleJWT
from rest_framework_simplejwt.exceptions import TokenError


# Custom
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    SignoutSerializer,
    ProfileSerializer,
)
from .authentication import UserAuthenticationView, CookieJWTAuthentication


# 회원가입
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Signup is successful'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    message = '로그인 완료'
    status_code = status.HTTP_200_OK

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return UserAuthenticationView.set_token_cookies(self, user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        access_token = request.COOKIES.get('access')

        if refresh_token is None and access_token is None:
            raise AuthenticationFailed('로그인한 사용자가 아닙니다.')

        # 로그아웃 후 쿠키 삭제
        res = Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK,
        )
        res.delete_cookie('access')
        res.delete_cookie('refresh')
        return res


# 회원탈퇴
class SignoutView(APIView):
    authentication_classes = (CookieJWTAuthentication,)

    def post(self, request):
        serializer = SignoutSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            user = request.user
            user.is_active = False
            user.save()
            # 로그아웃 처리
            res = Response({'message': '회원 탈퇴'}, status=status.HTTP_200_OK)
            res.delete_cookie('access')
            res.delete_cookie('refresh')
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 회원조회
class ProfileView(APIView):
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


# 회원수정
class UserUpdateView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
