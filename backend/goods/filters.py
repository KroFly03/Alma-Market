import django_filters
from django_filters import filters

from goods.models import Item


class ItemFilter(django_filters.FilterSet):
    price = filters.RangeFilter(field_name='price')
    category = filters.CharFilter(field_name='category', lookup_expr='exact')
    manufacturer = filters.CharFilter(field_name='manufacturer', lookup_expr='exact')
    sub_category = filters.CharFilter(field_name='category__subcategory__id', lookup_expr='exact')

    class Meta:
        model = Item
        fields = ('price', 'category', 'manufacturer', 'sub_category')
