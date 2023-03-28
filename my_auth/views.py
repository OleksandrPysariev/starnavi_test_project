from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, permissions, status
from rest_framework.response import Response

from my_auth.models import User
from .apischemas import login_schema, refresh_token_schema
from .authentication import JWTAuthentication
from .serializers import RegisterSerializer, ObtainTokenSerializer, RefreshTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class ObtainTokenPairView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    @swagger_auto_schema(request_body=login_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        access_token = JWTAuthentication.create_jwt(user, "access")
        refresh_token = JWTAuthentication.create_jwt(user, "refresh")

        user.user_activity.set_last_login()

        return Response({"access": access_token, "refresh": refresh_token})


class TokenRefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenSerializer

    @swagger_auto_schema(request_body=refresh_token_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get("refresh")
        access_token, refresh_token = JWTAuthentication.refresh_jwt(refresh)
        return Response({"access": access_token, "refresh": refresh_token})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
