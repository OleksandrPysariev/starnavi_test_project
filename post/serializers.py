from rest_framework import serializers

from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body"]


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "created", "modified", "title", "body", "posted_by", "likes_count"]


