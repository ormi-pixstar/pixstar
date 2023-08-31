from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.state import token_backend
from django.contrib.auth import get_user_model

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
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
            },
            status=self.status_code,
        )

        # JWT 토큰을 쿠키에 저장
        res.set_cookie('access', access_token, httponly=True, secure=True)
        res.set_cookie('refresh', refresh_token, httponly=True, secure=True)
        return res


# 토큰 추출
class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')

        # 토큰이 있는지 확인
        if not access_token:
            raise AuthenticationFailed('토큰이 없습니다.')

        try:
            # 토큰 유효성 검사
            payload = token_backend.decode(access_token)
            user = User.objects.get(id=payload['user_id'])
            return (user, access_token)
        except TokenError:
            raise AuthenticationFailed('토큰이 유효하지 않습니다.')
        except User.DoesNotExist:
            raise AuthenticationFailed('사용자 정보를 찾을 수 없습니다.')
