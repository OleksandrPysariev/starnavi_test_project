from django.urls import path

from .views import LikeView

urlpatterns = [
    path("post", LikeView.as_view(), name="like_post_create"),
]
