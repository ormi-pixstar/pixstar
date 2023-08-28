from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer


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
        res.set_cookie("access", access_token, httponly=True, secure=True)
        res.set_cookie("refresh", refresh_token, httponly=True, secure=True)
        return res


class SignupView(UserAuthenticationView):
    message = "회원가입 성공"
    status_code = status.HTTP_201_CREATED

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return self.set_token_cookies(user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(UserAuthenticationView):
    message = "로그인 성공"
    status_code = status.HTTP_200_OK

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return self.set_token_cookies(user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
