from django.db import models
from django_extensions.db.models import TimeStampedModel
from my_auth.models import User
from post.models import Post


class Like(TimeStampedModel, models.Model):
    modified = None

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
