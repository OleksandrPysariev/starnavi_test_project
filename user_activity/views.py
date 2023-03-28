from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_auth.authentication import JWTAuthentication
from user_activity.serializers import UserActivitySerializer


class UserActivityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserActivitySerializer(self.request.user.user_activity).data, status=status.HTTP_200_OK)



