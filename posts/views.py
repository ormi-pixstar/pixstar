from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
class PostSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if query:
            posts = Post.objects.filter(title__icontains=query)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({"message": "Query parameter 'q' is required."})
    

class PostWrite(APIView):
    pass


class PostDetail(APIView):
    pass


class PostEdit(APIView):
    pass


class PostDelete(APIView):
    pass


class PostFeedback(APIView):
    pass