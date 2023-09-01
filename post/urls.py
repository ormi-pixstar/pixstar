from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path("list/", views.PostList.as_view(), name='list'),
    path("write/", views.PostWrite.as_view(), name='post-write'),
    path("detail/<int:pk>/", views.PostDetail.as_view(), name='post-detail'),
    path("detail/<int:pk>/edit/", views.PostEdit.as_view(), name='post-edit'),
    path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name='post-delete'),
    path("detail/<int:pk>/like/", views.PostLike.as_view(), name='post-like'),
    # S3이미지 업로드 테스트용
    path("test/image/", views.ImageUploadTest.as_view()),
    # 댓글
    path(
        'detail/<int:post_id>/comment/',
        views.CommentView.as_view(),
        name='comment_view',
    ),
    path(
        'detail/<int:post_id>/comment/<int:comment_id>',
        views.CommentDetailView.as_view(),
        name='comment_detail_view',
    ),
]
