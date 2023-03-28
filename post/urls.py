from django.urls import path

from .views import (
    CreatePostView,
    PostView,
    ListPostView,
)

urlpatterns = [
    path("create", CreatePostView.as_view(), name="post_create"),
    path("<int:pk>", PostView.as_view(), name="post_get"),
    path("all", ListPostView.as_view(), name="post_get_all")
]
