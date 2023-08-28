from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            res = Response(
                {
                    "message": "회원가입 성공",
                },
                status=status.HTTP_201_CREATED,
            )

            # JWT 토큰을 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True, secure=True)
            res.set_cookie("refresh", refresh_token, httponly=True, secure=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(TokenObtainPairView):
#     serializer_class = UserSerializer

#     def post(self, request):
#         response = super().post(request)
#         if response.status_code == status.HTTP_200_OK:
#             # 필요한 경우 여기에 추가적인 응답 데이터를 추가할 수 있습니다.
#             pass
#         return response
