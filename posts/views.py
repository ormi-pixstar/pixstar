from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer


## 포스트 검색
class PostSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if query:
            posts = Post.objects.filter(title__icontains=query)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({"message": "Query parameter 'q' is required."})


## 댓글 작성, 조회
class CommentView(APIView):
    def get(self, request, post_id):
            post = Post.objects.get(id=post_id)
            comments = post.comment_set.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.writer, post_id=post_id)
            return Response(serializer.data, status.HTTP_201_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## 댓글 수정, 삭제
class CommentDetailView(APIView):
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save() # post에 user 정보 있기 때문에 (user=request.user) 생략
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)