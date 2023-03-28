from typing import Optional, List

from django.contrib.auth.models import User
from django.db.models import Count

from post.models import Post
from post.serializers import CreatePostSerializer


class PostService:
    @staticmethod
    def create(serializer: CreatePostSerializer, user: User) -> Post:
        return serializer.save(posted_by=user)

    @staticmethod
    def get_by_pk(pk) -> Optional[Post]:
        result = Post.objects.annotate(likes_count=Count('like')).get(id=pk)
        return result

    @staticmethod
    def get_all() -> Optional[List[Post]]:
        return Post.objects.annotate(likes_count=Count('like')).order_by("-created").all()
