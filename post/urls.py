from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    # 포스트 목록 조회
    path("list/", views.PostListView.as_view(), name='post-list'),
    # 포스트 작성
    path("write/", views.PostWrite.as_view(), name='post-write'),
    # 포스트 상세 조회
    path("detail/<int:pk>/", views.PostDetail.as_view(), name='post-detail'),
    # path("detail/<int:pk>/edit/", views.PostEdit.as_view(), name='post-edit'),
    # path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name='post-delete'),
    # path("detail/<int:pk>/like/", views.PostLike.as_view(), name='post-like'),
]
