from rest_framework import serializers

from user_activity.models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ["last_login", "last_activity"]
