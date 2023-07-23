import json
from collections import OrderedDict
from types import NoneType

import pytest
from rest_framework import status

from goods.models import Characteristic
from tests.factories import ItemFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestUpdateItemView:
    base_url = 'goods:update_item'

    def test_return_correct_data_keys(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [
                {'name': char.characteristic.name, 'value': char.value}
                for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'characteristic', 'name', 'description', 'price', 'amount', 'image',
                                     'is_active', 'category', 'manufacturer']
        assert list(data.get('characteristic', None)[0].keys()) == ['id', 'name', 'value']

    def test_correct_status_code(self, client, login_user, login_admin, item):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, item.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(get_url(self.base_url, item.id),
                                HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'Необходимо быть администратором, чтобы выполнить данное действие.'

        response = client.patch(get_url(self.base_url, item.id), content_type='application/json',
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [
                {'name': char.characteristic.name, 'value': char.value}
                for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, list, str, str, int, int, NoneType, bool, int, int]

    def test_correct_validation_unique_name(self, client, login_admin, item):
        _, admin_access_token = login_admin
        new_item = ItemFactory.create()

        data = {
            'name': new_item.name,
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [
                {'name': char.characteristic.name, 'value': char.value}
                for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('name', None) == ['Товар с таким Название уже существует.']

    def test_correct_max_length_description_and_name(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test' * 30,
            'description': 'test' * 300,
            'price': 1000,
            'amount': 1,
            'characteristic': [{'name': char.characteristic.name, 'value': char.value}
                               for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('name', None) == ['Убедитесь, что это значение содержит не более 100 символов.']
        assert data.get('description', None) == ['Убедитесь, что это значение содержит не более 1000 символов.']

    def test_correct_new_characteristic_update(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [{'name': 'test', 'value': 'test'}],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('characteristic', None)[::-1][0].get('id', None)

        assert Characteristic.objects.get(pk=data)

    def test_correct_update(self, client, login_admin, item):
        _, admin_access_token = login_admin
        new_item = ItemFactory.create()

        char = item.itemcharacteristic_set.first()

        data = {
            'name': 'new_test',
            'description': 'new_test',
            'price': 500,
            'amount': 10,
            'characteristic': [
                {'id': char.characteristic.id, 'name': char.characteristic.name, 'value': 'test'},
            ],
            'category': new_item.category.id,
            'manufacturer': new_item.manufacturer.id
        }

        response = client.patch(
            get_url(self.base_url, item.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')
        print(response.data)
        assert response.data.get('characteristic', None) == data.get('characteristic')
        assert response.data.get('name', None) == data.get('name')
        assert response.data.get('price', None) == data.get('price')
        assert response.data.get('amount', None) == data.get('amount')
        assert response.data.get('category', None) == data.get('category')
        assert response.data.get('manufacturer', None) == data.get('manufacturer')
