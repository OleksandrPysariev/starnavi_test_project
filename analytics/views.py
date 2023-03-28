from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from analytics.pagination import LikesActivityPagination
from analytics.serializers import LikesActivitySerializer
from analytics.filters import LikesActivityFilter
from like.models import Like
from my_auth.authentication import JWTAuthentication


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class LikesActivityView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    model = Like
    serializer_class = LikesActivitySerializer
    pagination_class = LikesActivityPagination
    queryset = Like.objects\
        .annotate(day=TruncDay("created"))\
        .values("day")\
        .annotate(count=Count("id"))\
        .values("day", "count")\
        .order_by("-day")
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikesActivityFilter

