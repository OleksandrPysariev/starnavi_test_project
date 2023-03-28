from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from facebook.permissions import ReadOnly
from my_auth.authentication import JWTAuthentication
from .models import Post
from .pagination import PostsPagination
from .serializers import CreatePostSerializer, PostSerializer
from .apischemas import create_post_schema
from .service import PostService


class CreatePostView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=create_post_schema)
    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            PostService.create(serializer, self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):

    permission_classes = [ReadOnly]

    def get(self, request, pk):
        try:
            post = PostService.get_by_pk(pk)
            serializer = PostSerializer(post)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPostView(ListAPIView):

    permission_classes = [ReadOnly]

    queryset = PostService.get_all()
    serializer_class = PostSerializer
    pagination_class = PostsPagination

