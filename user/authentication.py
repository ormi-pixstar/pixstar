from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.state import token_backend
from django.contrib.auth.backends import ModelBackend
# from .models import User

from django.contrib.auth import get_user_model
User = get_user_model()


# 토큰 추출
class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')

        # 토큰이 있는지 확인
        if not access_token:
            raise AuthenticationFailed('Token is missing.')

        try:
            # 토큰 유효성 검사
            payload = token_backend.decode(access_token)
            user = User.objects.get(id=payload['user_id'])
            return (user, access_token)
        except TokenError:
            raise AuthenticationFailed('Token is invalid.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None