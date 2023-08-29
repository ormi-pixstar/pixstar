from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.authentication import CookieJWTAuthentication
from django.shortcuts import get_object_or_404
import boto3
import os
from drf_spectacular.utils import extend_schema
from .models import Post, Image, Comment
from .serializers import (
    PostSerializer,
    ImageSerializer,
    LikeSerializer,
    CommentSerializer,
)
from django.db.models import Count
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


class Pagination(PageNumberPagination):
    page_size = 5  # 페이지당 보여줄 포스트 수
    page_size_query_param = 'page_size'  # 페이지 크기를 지정하는 쿼리 파라미터
    max_page_size = 100  # 최대 페이지 크기


# 포스트 조회 및 검색
class PostList(APIView):
    pagination_class = Pagination

    # 검색 쿼리 처리
    def search_posts(self, search_query):
        if search_query:
            if search_query[0] == '@':  # user 검색
                username = search_query[1:]
                return Post.objects.filter(writer__username__icontains=username)
            else:  # 포스트 검색
                return Post.objects.filter(content__icontains=search_query)
        return Post.objects.all()  # 전체 조회

    # 정렬 쿼리 처리
    def order_posts(self, posts, sort_order):
        if sort_order == 'asc':
            return posts.order_by('created_at')
        elif sort_order == 'likes':
            return posts.annotate(like_count=Count('like')).order_by('-like_count')
        return posts.order_by('-created_at')

    @extend_schema(responses=PostSerializer)
    def get(self, request):
        # 쿼리 파라미터 가져오기
        search_query = request.query_params.get('search', None)
        sort_order = request.query_params.get('sort', 'desc')

        # 검색어에 맞는 포스트 가져오기
        posts = self.search_posts(search_query)

        # 조건에 맞춰서 정렬
        posts = self.order_posts(posts, sort_order)

        # 페이지 객체 생성 및 데이터 시리얼라이징
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(page, many=True)

        response_data = {
            'results': serializer.data,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PostWrite(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        user = request.user

        # 토큰 확인
        if not user.is_authenticated:
            return Response(
                {'detail': 'User is not authenticated.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = PostSerializer(data=request.data, context={"request": request})
        print(serializer.context)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(
                {'message': 'Successfully created post'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostEdit(APIView):
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(
            post, context={"request": request}, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDelete(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status.HTTP_204_NO_CONTENT)
