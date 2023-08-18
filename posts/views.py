from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


# 포스트 조회 및 검색
class PostListAPIView(APIView):
    def get(self, request):
        # 쿼리 파라미터 가져오기
        search_query = request.query_params.get('search', None)
        sort_order = request.query_params.get('sort', None)

        # 검색 쿼리 처리
        if search_query:
            posts = Post.objects.filter(content__icontains=search_query)
        else:
            posts = Post.objects.all()

        # 정렬 쿼리 처리
        if sort_order == 'desc':
            posts = posts.order_by('-created_at')
        elif sort_order == 'likes':
            posts = posts.order_by('-likes')

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
