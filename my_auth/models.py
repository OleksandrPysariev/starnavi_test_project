from django.db import models
from django.contrib.auth.models import AbstractUser
from user_activity.models import UserActivity


class User(AbstractUser):
    last_login = None
    date_joined = None

    user_activity = models.OneToOneField(UserActivity, on_delete=models.CASCADE, related_name="user_activity")
