import json

import pytest
from rest_framework import status

from tests.factories import ItemFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestAddBasketItemView:
    base_url = 'baskets:add_basket_item'

    def test_return_correct_data_keys(self, client, login_user):
        _, user_access_token = login_user

        item = ItemFactory.create()

        initial_data = {
            'item': item.id,
            'amount': 1,
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert list(response.data.keys()) == ['item', 'amount']

    def test_correct_return_status_code(self, client, login_user):
        _, user_access_token = login_user

        item = ItemFactory.create()

        initial_data = {
            'item': item.id,
            'amount': 1,
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Учетные данные не были предоставлены.'

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client, login_user):
        _, user_access_token = login_user

        item = ItemFactory.create()

        initial_data = {
            'item': item.id,
            'amount': 1,
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert [type(elem) for elem in response.data.values()] == [int, int]

    def test_correct_require_field_validation(self, client, login_user):
        _, user_access_token = login_user

        response = client.post(
            get_url(self.base_url), data={}, content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data

        assert data.get('item', []) == ['Обязательное поле.']
        assert data.get('amount', []) == ['Обязательное поле.']

    def test_correct_unique_item_validation(self, client, login_user, item):
        _, user_access_token = login_user

        initial_data = {
            'item': item.id,
            'amount': 1,
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.data.get('non_field_errors', None) == [
            'Поля user, item должны производить массив с уникальными значениями.']

    def test_correct_negative_amount_check(self, client, login_user):
        _, user_access_token = login_user

        item = ItemFactory.create()

        initial_data = {
            'item': item.id,
            'amount': -1,
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.data.get('amount', None) == ['Убедитесь, что это значение больше либо равно 0.']

    def test_correct_create(self, client, login_user):
        _, user_access_token = login_user

        item = ItemFactory.create()

        initial_data = {
            'item': item.id,
            'amount': 1
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.data.get('item', None) == item.id
        assert response.data.get('amount', None) == initial_data.get('amount', None)
