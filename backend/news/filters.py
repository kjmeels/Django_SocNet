from django_filters import rest_framework as filters

from news.models import News


class NewFilter(filters.FilterSet):
    text_filter = filters.CharFilter(field_name="text", lookup_expr="contains")
    created_at_filter = filters.DateFilter(field_name="created_at", lookup_expr="contains")

    class Meta:
        model = News
        fields = [
            "text_filter",
            "created_at_filter",
        ]
