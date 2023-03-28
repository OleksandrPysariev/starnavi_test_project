from typing import Optional, List, Type
from abc import ABC, abstractmethod

from django.contrib.auth.models import User

from like.models import Like
from like.serializers import LikeSerializer
from facebook.result import Result
from post.models import Post


class BasePolicy(ABC):
    @abstractmethod
    def is_allowed(self):
        pass


class SameUserLikePolicy(BasePolicy):
    """
    Enable this policy to prohibit likes for your own posts
    """
    def __init__(self, serializer: LikeSerializer, user: User):
        self.serializer = serializer
        self.user = user

    def get_poster(self) -> User:
        return self.serializer.validated_data["post"].posted_by

    @property
    def is_allowed(self) -> bool:
        return self.get_poster() != self.user


class LikeService:
    # Add or remove like policies here. To extend like policy write a new class which should inherit from BasePolicy
    # and define all of its abstract methods
    like_policies: List[Type[BasePolicy]] = []

    @staticmethod
    def get(post_id: int, user_id: int) -> Optional[Like]:
        try:
            return Like.objects.get(post_id=post_id, user_id=user_id)
        except Like.DoesNotExist:
            return

    @staticmethod
    def is_allowed(serializer: LikeSerializer, user: User):
        return all([policy(serializer, user).is_allowed for policy in LikeService.like_policies])

    @staticmethod
    def create(serializer, user: User) -> Result:
        if not LikeService.is_allowed(serializer, user):
            return Result.Fail("This action is not allowed.")
        if like := LikeService.get(serializer.validated_data["post"].pk, user.pk):
            LikeService.deduct_like(like)
        else:
            LikeService.add_like(serializer, user)
        return Result.Ok()

    @staticmethod
    def add_like(serializer: LikeSerializer, user: User):
        serializer.save(user=user)

    @staticmethod
    def deduct_like(like: Like):
        like.delete()
