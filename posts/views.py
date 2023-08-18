from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count
from drf_spectacular.utils import extend_schema


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
