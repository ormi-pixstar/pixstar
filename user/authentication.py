# 토큰 추출
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('access')
        if not jwt_token:
            return None

        return super().authenticate(request)
