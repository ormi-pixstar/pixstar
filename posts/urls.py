from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("list/", views.PostList.as_view(), name='list'),
    path("write/", views.PostWrite.as_view(), name='post-write'),
    path("detail/<int:pk>/", views.PostDetail.as_view(), name='post-detail'),
    path("detail/<int:pk>/edit/", views.PostEdit.as_view(), name='post-edit'),
    path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name='post-delete'),
    path("detail/<int:pk>/like", views.PostLike.as_view(), name='post-like'),
]
