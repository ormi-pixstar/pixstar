from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import boto3
import os
from drf_spectacular.utils import extend_schema
from .models import Post, Image
from .serializers import PostSerializer, ImageSerializer, PostLikeSerializer
from django.db.models import Count
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


# 포스트 조회 및 검색
class PostList(APIView):

    # 검색 쿼리 처리
    def search_posts(self, search_query):
        if search_query:
            return Post.objects.filter(content__icontains=search_query)
        return Post.objects.all()

    # 정렬 쿼리 처리
    def order_posts(self, posts, sort_order):
        if sort_order == 'asc':
            return posts.order_by('created_at')
        elif sort_order == 'likes':
            return posts.order_by('-likes_count')
        return posts.order_by('-created_at')

    @extend_schema(responses=PostSerializer)
    def get(self, request):
        # 쿼리 파라미터 가져오기
        search_query = request.query_params.get('search', None)
        sort_order = request.query_params.get('sort', 'desc')

        # 검색어에 맞는 포스트 가져오기
        posts = self.search_posts(search_query)
        # likes_count를 response에 언제나 포함
        posts = posts.annotate(likes_count=Count('like'))
        # 조건에 맞춰서 정렬
        posts = self.order_posts(posts, sort_order)

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostWrite(APIView):
    def post(self, request):
        serializer = PostSerializer(context={"request": request}, data=request.data)
        if serializer.is_valid():
            print(serializer)
            print(request.data)
            post = serializer.save(writer=request.user)
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostEdit(APIView):
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDelete(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        if serializer.is_valid():
            post.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLike(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.like.all():
            post.like.remove(request.user)
            return Response("unlike", status = status.HTTP_200_OK)
        post.like.add(request.user)
        return Response("like", status = status.HTTP_200_OK)


# 이미지 업로드 TEST용, 배포 시 삭제
class ImageUploadTest(APIView):
    parser_classes = (MultiPartParser,)

    @extend_schema(request={"file": {"type": "file"}}, responses={201: None})
    def post(self, request):
        file_obj = request.FILES.get('file')
        # print(request.FILES)
        if not file_obj:
            return Response({"error": "파일이 없습니다."}, status=400)

        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3 = boto3.client('s3')
        s3.upload_fileobj(file_obj, bucket_name, file_obj.name)

        return Response(status=201)
