from collections import OrderedDict

import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestListBasketView:
    base_url = 'baskets:list_basket_item'

    def test_return_correct_data_keys(self, client, login_user):
        user, user_access_token = login_user

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        basket_data = response.data[0]
        item_data = basket_data.get('item', None)

        assert list(basket_data.keys()) == ['item', 'amount']
        assert len(basket_data.keys()) == 2

        assert list(item_data.keys()) == ['id', 'category', 'manufacturer', 'name', 'price', 'image',
                                          'is_active']
        assert len(item_data.keys()) == 7

    def test_correct_return_status_code(self, client, login_user):
        _, user_access_token = login_user

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_user):
        user, user_access_token = login_user

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        basket_data = response.data[0]
        item_data = basket_data.get('item', None)

        assert [type(elem) for elem in basket_data.values()] == [OrderedDict, int]
        assert [type(elem) for elem in item_data.values()] == [int, str, str, str, int, str, bool]
