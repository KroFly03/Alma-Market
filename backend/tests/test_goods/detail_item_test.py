from collections import OrderedDict
from types import NoneType

import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestDetailItemView:
    base_url = 'goods:detail_item'
    
    def test_return_correct_data_keys(self, client, item):
        response = client.get(get_url(self.base_url, item.id))

        data = response.data

        assert list(data.keys()) == ['id', 'characteristic', 'category', 'manufacturer', 'name', 'description',
                                     'price', 'amount', 'image', 'is_active']
        assert list(data.get('manufacturer', None).keys()) == ['id', 'total_goods', 'name']
        assert list(data.get('category', None).keys()) == ['id', 'total_goods', 'subcategory', 'name']
        assert list(data.get('category', None).get('subcategory', None)[0].keys()) == ['id', 'name']
        assert list(data.get('characteristic', None)[0].keys()) == ['id', 'name', 'value']

    def test_correct_status_code(self, client, item):
        response = client.get(get_url(self.base_url, 10000))

        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get(get_url(self.base_url, item.id))

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_type(self, client, item):
        response = client.get(get_url(self.base_url, item.id))

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, list, OrderedDict, OrderedDict, str, str, int, int,
                                                          str, bool]

    def test_correct_detail_item(self, client, item):
        response = client.get(get_url(self.base_url, item.id))

        assert response.data.get('id', None) == item.id
