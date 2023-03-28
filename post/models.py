from django.db import models
from django_extensions.db.models import TimeStampedModel
from my_auth.models import User


class Post(TimeStampedModel, models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    body = models.TextField()

    def __str__(self):
        return f"'{self.title}' by {self.posted_by}"
