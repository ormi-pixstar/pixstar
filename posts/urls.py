from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("list/", views.PostListAPIView.as_view(), name='list'),
]
