# pixstar

## 변경점
 ### myapp/settings.py
  - DB sqlite3로 임시 사용
  - INSTALLED_APPS
   - package : sslserver 주석처리
   - users > user, posts > post 변경후 주석처리
  - REST_Framework 인증은 simplejwt의 JWTAuthentication으로 변경
  - PERMISSION은 AllowAny로 설정
  - SIMPLE_JWT는 기존 것을 주석 후 변경사항을 하단에 추가
 
 ### myapp/urls.py
  - user와 post 연결 변경 및 post 주석
  - urlpatterns에 추가로 Media Dir연결은 추후 협의

 ### user app
  - 일부 파일 제거
  
  - authentication.py 추가
  
  - models.py : name필드 제외
  
  - serializers.py, views.py 예외처리가 적용된 코드로 수정
  - urls.py, views.py 회원조회는 임시로 주석처리

  