from django_filters import rest_framework as filters

from users.constants import GenderChoices
from users.models import User


class UserFilter(filters.FilterSet):
    age = filters.RangeFilter(field_name="age")
    # age__gt = filters.NumberFilter(field_name="age", lookup_expr="gt")
    # age__lt = filters.NumberFilter(field_name="age", lookup_expr="lt")
    city = filters.CharFilter(field_name="city__slug")
    gender = filters.ChoiceFilter(choices=GenderChoices.choices)
    languages = filters.CharFilter(field_name="languages__language_name")

    class Meta:
        model = User
        fields = ["age", "city", "full_name"]
