from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import SignupSerializer, LoginSerializer


# 토큰 발급
class UserAuthenticationView(APIView):
    def set_token_cookies(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        res = Response(
            {
                "message": self.message,
            },
            status=self.status_code,
        )

        # JWT 토큰을 쿠키에 저장
        res.set_cookie(
            "access",
            access_token,
            httponly=True,
            secure=True,
        )
        res.set_cookie(
            "refresh",
            refresh_token,
            httponly=True,
            secure=True,
        )
        return res


# 회원가입
class SignupView(UserAuthenticationView):
    message = "회원가입 성공"
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
    message = "로그인 성공"
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
                    {"detail": "User already logout"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 토큰을 검증하고 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()

            # 로그아웃 후 쿠키 삭제
            res = Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK,
            )
            res.delete_cookie("access")
            res.delete_cookie("refresh")
            return res

        except TokenError:
            return Response(
                {"detail": "Token is invalid or expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
