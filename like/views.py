from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from like.apischemas import like_action_schema
from like.serializers import LikeSerializer
from like.service import LikeService
from my_auth.authentication import JWTAuthentication


class LikeView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=like_action_schema)
    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = LikeService.create(serializer, self.request.user)
        if result.failure:
            return Response({"error": result.error})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

