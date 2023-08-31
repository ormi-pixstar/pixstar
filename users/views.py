from django.contrib.auth import get_user_model

# DjangoRestFramework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

# DjangroRestFramework-simpleJWT
from rest_framework_simplejwt.exceptions import TokenError

# Custom
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    PasswordCheckSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
)
from .authentication import UserAuthenticationView, CookieJWTAuthentication

User = get_user_model()


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
        serializer = PasswordCheckSerializer(
            data=request.data, context={'request': request}
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


# 프로필 조회 및 수정
class ProfileView(APIView):
    def get(self, request, user_id):
        if not user_id:
            return Response(
                {"detail": "user_id 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "해당 사용자가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    authentication_classes = (CookieJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        serializer = ProfileUpdateSerializer(
            instance=request.user,
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': '프로필 수정 완료'},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
