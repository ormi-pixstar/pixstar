from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    # 게시글 목록
    path("list/", views.PostList.as_view(), name='list'),
    # 게시글 작성
    path("write/", views.PostWrite.as_view(), name='post-write'),
    # 게시글 상세 조회
    path("detail/<int:pk>/", views.PostDetail.as_view(), name='post-detail'),
    # 게시글 수정
    path("detail/<int:pk>/edit/", views.PostEdit.as_view(), name='post-edit'),
    # 게시글 삭제
    path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name='post-delete'),
    # 게시글 좋아요
    path("detail/<int:pk>/like/", views.PostLike.as_view(), name='post-like'),
    # # 댓글 조회, 작성
    # path(
    #     'detail/<int:post_id>/comment/',
    #     views.CommentView.as_view(),
    #     name='comment',
    # ),
    # # 대댓글 작성 및 댓글 수정, 삭제
    # path(
    #     'detail/<int:post_id>/comment/<int:comment_id>',
    #     views.CommentDetailView.as_view(),
    #     name='',
    # ),
]
