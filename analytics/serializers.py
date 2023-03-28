from rest_framework import serializers

from like.models import Like


class LikesActivitySerializer(serializers.ModelSerializer):
    day = serializers.DateTimeField(format="%d-%m-%Y")
    count = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ["day", "count"]
        read_only_fields = ["day", "count"]
