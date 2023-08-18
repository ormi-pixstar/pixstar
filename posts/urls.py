from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("list/", views.PostSearchAPIView.as_view(), name='list'),
]
