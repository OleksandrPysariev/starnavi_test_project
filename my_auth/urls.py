from django.urls import path
from my_auth.views import ObtainTokenPairView, RegisterView, TokenRefreshView


urlpatterns = [
    path('login', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
]