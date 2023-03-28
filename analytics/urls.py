from django.urls import path

from .views import LikesActivityView

urlpatterns = [
    path("likes", LikesActivityView.as_view(), name="likes_activity"),
]
