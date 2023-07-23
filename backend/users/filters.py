import django_filters
from django_filters import filters
from users.models import User


class UserFilter(django_filters.FilterSet):
    email = filters.CharFilter(field_name='phone', lookup_expr='startswith')

    class Meta:
        model = User
        fields = ('phone',)
