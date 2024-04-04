from django_filters import rest_framework as filters

from users.constants import GenderChoices
from users.models import User


class UserFilter(filters.FilterSet):
    age = filters.RangeFilter(field_name="age")
    city = filters.CharFilter(field_name="city__slug")
    gender = filters.ChoiceFilter(choices=GenderChoices.choices)
    language = filters.CharFilter(field_name="languages__language_name")

    class Meta:
        model = User
        fields = ["age", "city", "full_name"]
