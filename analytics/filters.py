from django_filters import rest_framework as filters

from like.models import Like


class LikesActivityFilter(filters.FilterSet):
    from_date = filters.DateFilter(input_formats=["%d-%m-%Y"], field_name="created", lookup_expr="gte")
    to_date = filters.DateFilter(input_formats=["%d-%m-%Y"], field_name="created", lookup_expr="lte")

    class Meta:
        model = Like
        fields = ["from_date", "to_date"]
