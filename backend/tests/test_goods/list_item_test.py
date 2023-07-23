import math
from collections import OrderedDict
from types import NoneType

import pytest
from rest_framework import status

from paginations import GoodPagination
from tests.factories import ItemFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListItemView:
    base_url = 'goods:list_item'
    
    def test_pagination_keys(self, client):
        ItemFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert list(response.data.keys()) == ['links', 'count', 'total_pages', 'current_page', 'results']

    def test_return_correct_data_keys(self, client):
        ItemFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data.get('results', None)[0]

        assert list(data.keys()) == ['id', 'characteristic', 'category', 'manufacturer', 'name', 'description',
                                     'price', 'amount', 'image', 'is_active']
        assert list(data.get('manufacturer', None).keys()) == ['id', 'total_goods', 'name']
        assert list(data.get('category', None).keys()) == ['id', 'total_goods', 'subcategory', 'name']
        assert list(data.get('category', None).get('subcategory', None)[0].keys()) == ['id', 'name']
        assert list(data.get('characteristic', None)[0].keys()) == ['id', 'name', 'value']

    def test_correct_status_code(self, client):
        ItemFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_amount(self, client):
        amount = 15

        ItemFactory.create_batch(15)

        response = client.get(get_url(self.base_url))

        assert len(response.data.get('results', None)) == amount

    def test_correct_data_type(self, client):
        ItemFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data.get('results', None)[0]

        assert [type(elem) for elem in data.values()] == [int, list, OrderedDict, OrderedDict, str, str, int, int,
                                                          NoneType, bool]

    def test_pagination_pages(self, client):
        amount = 46

        ItemFactory.create_batch(amount)

        response = client.get(get_url(self.base_url))

        data = response.data

        assert data.get('count', None) == amount
        assert data.get('total_pages', None) == math.ceil(amount / GoodPagination.page_size)

    def test_pagination_links(self, client):
        amount = 46
        page = 2

        ItemFactory.create_batch(amount)

        response = client.get(get_url(self.base_url, page=page))

        data = response.data

        assert data.get('links', None) == {'previous': 'http://testserver/api/goods',
                                           'next': 'http://testserver/api/goods?page=3'}
        assert data.get('current_page', None) == page

    def test_category_filter(self, client):
        items = ItemFactory.create_batch(10)

        category_id = items[0].category.id

        response = client.get(get_url(self.base_url, category=category_id))

        data = response.data.get('results', None)

        assert data[0].get('category', None).get('id', None) == category_id
        assert len(data) == 1

    def test_manufacturer_filter(self, client):
        items = ItemFactory.create_batch(10)

        manufacturer_id = items[0].manufacturer.id

        response = client.get(get_url(self.base_url, manufacturer=manufacturer_id))

        data = response.data.get('results', None)

        assert data[0].get('manufacturer', None).get('id', None) == manufacturer_id
        assert len(data) == 1

    def test_price_filter(self, client):
        price_max = 500
        price_min = 1500

        ItemFactory.create_batch(10)

        response = client.get(get_url(self.base_url, price_min=price_min))

        data = response.data.get('results', None)

        assert data == []

        response = client.get(get_url(self.base_url, price_max=price_max))

        data = response.data.get('results', None)

        assert data == []

        response = client.get(get_url(self.base_url, price_min=price_max))

        data = response.data.get('results', None)

        assert data != []

        response = client.get(get_url(self.base_url, price_max=price_min))

        data = response.data.get('results', None)

        assert data != []

    def test_name_filter(self, client):
        items = ItemFactory.create_batch(10)

        name = items[0].name

        response = client.get(get_url(self.base_url, search=name))

        data = response.data.get('results', None)

        assert data[0].get('name', None) == name
        assert len(data) == 1

    def test_id_ordering(self, client):
        ItemFactory.create_batch(10)

        response = client.get(get_url(self.base_url))

        data = response.data.get('results', None)

        assert data[0].get('id', None) > data[::-1][0].get('id', None)

    # def test_sub_category_filter(self, client):
    #     items = ItemFactory.create_batch(10)
    #
    #     sub_category = [sub_cat.id for sub_cat in items[0].category.subcategory.all()]
    #
    #     response = client.get(get_url(self.base_url, sub_category=sub_category))
    #
    #     data = response.data.get('results', None)
    #
    #     assert data[0].get('category', None).get('subcategory', None)[0].get('id', None) in sub_category
    #     assert len(data) == 1
