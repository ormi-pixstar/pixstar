from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from drf_standardized_errors.handler import exception_handler
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import boto3
import os
from drf_spectacular.utils import extend_schema
from .models import Post, Image, Comment
from .serializers import (
    PostSerializer,
    ImageSerializer,
    PostLikeSerializer,
    CommentSerializer,
)
from django.db.models import Count
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
import jwt
from rest_framework_simplejwt.tokens import AccessToken
from myapp.settings import SECRET_KEY
from .storage import S3Storage
from django.http import Http404


User = get_user_model()

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
    def post(self, request):
        serializer = PostSerializer(context={"request": request}, data=request.data)
        if serializer.is_valid():
            prefer = AccessToken(request.COOKIES["access"])['user_id']
            user = User.objects.get(id=prefer)
            post = serializer.save(writer=user)
            post.save()
            return Response(status=status.HTTP_201_CREATED)
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
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDelete(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        images = Image.objects.filter(post=post)
        s = S3Storage()
        for image in images:
            s.delete(image)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLike(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        prefer = AccessToken(request.COOKIES["access"])['user_id']
        user = User.objects.get(id=prefer)
        if user in post.like.all():
            post.like.remove(user)
            return Response("unlike", status=status.HTTP_200_OK)
        post.like.add(user)
        return Response("like", status=status.HTTP_200_OK)


# comment 조회, 작성
class CommentView(APIView):
    def get_exception_handler(self):
        return exception_handler
    
    # comment 조회
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.filter(parent=None, post_id=post)
            serializer = CommentSerializer(comment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='게시글을 찾을 수 없습니다.', code=404)

    # comment 작성
    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            serializer = CommentSerializer(data=request.data)

            if request.COOKIES.get('access') is None:
                raise exceptions.AuthenticationFailed('로그인한 사용자가 아닙니다.', code=401)
            else:
                prefer = AccessToken(request.COOKIES["access"])['user_id']
                user = User.objects.get(id=prefer)
            
            if serializer.is_valid():  # 유효성 검사
                serializer.save(writer=user, post_id=post.pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise exceptions.ValidationError(detail='댓글을 입력해주세요', code=400)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='게시글을 찾을 수 없습니다.', code=404)


# recomment 작성 및 comemnt의 수정, 삭제
class CommentDetailView(APIView):
    def get_exception_handler(self):
        return exception_handler
    
    # recomment 작성
    def post(self, request, post_id, comment_id):
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.get(pk=comment_id)
            serializer = CommentSerializer(data=request.data)

            if request.COOKIES.get('access') is None:
                raise exceptions.AuthenticationFailed('로그인한 사용자가 아닙니다.', code=401)
            else:
                prefer = AccessToken(request.COOKIES["access"])['user_id']
                user = User.objects.get(id=prefer)

            if serializer.is_valid():  # 유효성 검사
                serializer.save(writer=user, parent=comment, post_id=post.pk)  # 저장
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise exceptions.ValidationError(detail='댓글을 입력해주세요', code=400)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='게시글을 찾을 수 없습니다.', code=404)
        except Comment.DoesNotExist:
            raise exceptions.NotFound(detail='댓글을 찾을 수 없습니다.', code=404)

    # comment 수정
    def put(self, request, post_id, comment_id):
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.get(pk=comment_id)
            serializer = CommentSerializer(comment, data=request.data)

            if request.COOKIES.get('access') is None:
                raise exceptions.AuthenticationFailed('로그인한 사용자가 아닙니다.', code=401)
            else:
                prefer = AccessToken(request.COOKIES["access"])['user_id']
                user = User.objects.get(id=prefer)

            if user == comment.writer:
                if serializer.is_valid():
                    serializer.save(writer=user, post_id=post.pk)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise exceptions.ValidationError(detail='댓글을 입력해주세요', code=400)
            else:
                raise exceptions.AuthenticationFailed(detail='댓글 수정 권한이 없습니다.', code=403)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='게시글을 찾을 수 없습니다.', code=404)
        except Comment.DoesNotExist:
            raise exceptions.NotFound(detail='댓글을 찾을 수 없습니다.', code=404)

    # comment 삭제
    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(post_id=post_id, id=comment_id)

            if request.COOKIES.get('access') is None:
                raise exceptions.AuthenticationFailed('로그인한 사용자가 아닙니다.', code=401)
            else:
                prefer = AccessToken(request.COOKIES["access"])['user_id']
                user = User.objects.get(id=prefer)

            if user == comment.writer:
                comment.delete()
                return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
            else:
                raise exceptions.AuthenticationFailed(detail='댓글 삭제 권한이 없습니다.', code=403)
        except Comment.DoesNotExist:
            raise exceptions.NotFound(detail='댓글을 찾을 수 없습니다.', code=404)
