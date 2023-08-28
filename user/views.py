from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    SignoutSerializer,
    UserUpdateSerializer,
)
from post.serializers import UserPostSerializer

User = get_user_model()


# 토큰 발급
class UserAuthenticationView(APIView):
    def set_token_cookies(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        res = Response(
            {
                'message': self.message,
            },
            status=self.status_code,
        )

        # JWT 토큰을 쿠키에 저장
        res.set_cookie('access', access_token, httponly=True, secure=True)
        res.set_cookie('refresh', refresh_token, httponly=True, secure=True)
        return res


# 토큰 추출
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('access')
        if not jwt_token:
            return None

        # 임시로 Authorization 헤더를 설정
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {jwt_token}'

        return super().authenticate(request)


# 회원가입
class SignupView(UserAuthenticationView):
    message = '회원가입 성공'
    status_code = status.HTTP_201_CREATED

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return self.set_token_cookies(user)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# 로그인
class LoginView(UserAuthenticationView):
    message = '로그인 성공'
    status_code = status.HTTP_200_OK

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return self.set_token_cookies(user)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh')

            if refresh_token is None:
                return Response(
                    {'detail': 'User already logout'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 토큰을 검증하고 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()

            # 로그아웃 후 쿠키 삭제
            res = Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_200_OK,
            )
            res.delete_cookie('access')
            res.delete_cookie('refresh')
            return res

        except TokenError:
            return Response(
                {'detail': 'Token is invalid or expired.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# 회원탈퇴
class SignoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        user = request.user
        serializer = SignoutSerializer(data=request.data)

        # 토큰 확인
        if not user.is_authenticated:
            return Response(
                {'detail': 'User is not authenticated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 비밀번호 확인
        if not serializer.is_valid():
            return Response(
                {'detail': 'Password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 유저 비활성화(탈퇴)
        user.is_active = False
        user.save()

        return Response(
            {'message': 'Successfully deleted account'},
            status=status.HTTP_200_OK,
        )


# 유저 프로필 조회
class ProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserPostSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 유저 정보 수정
class UserUpdateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(data=request.data)

        # 토큰 확인
        if not user.is_authenticated:
            return Response(
                {'detail': 'User is not authenticated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 비밀번호 확인
        if not serializer.is_valid():
            return Response(
                {'detail': 'Incorrect password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
