import json
from collections import OrderedDict
from types import NoneType
import pytest
from rest_framework import status

from goods.models import Characteristic
from tests.utils import get_url


@pytest.mark.django_db()
class TestCreateItemView:
    base_url = 'goods:create_item'

    def test_return_correct_data_keys(self, client, login_admin, item, media_root):
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

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'characteristic', 'name', 'description', 'price', 'amount', 'image',
                                     'is_active', 'category', 'manufacturer']
        assert list(data.get('characteristic', None)[0].keys()) == ['id', 'name', 'value']

    def test_correct_status_code(self, client, login_user, login_admin, item):
        _, user_access_token = login_user
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

        response = client.post(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.post(get_url(self.base_url),
                               HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'Необходимо быть администратором, чтобы выполнить данное действие.'

        response = client.post(get_url(self.base_url), data={},
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_201_CREATED

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

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, list, str, str, int, int, str, bool, int, int]

    def test_correct_validation_require_field(self, client, login_admin, item):
        _, admin_access_token = login_admin

        response = client.post(
            get_url(self.base_url), data={}, content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('characteristic', []) == ['Обязательное поле.']
        assert data.get('name', []) == ['Обязательное поле.']
        assert data.get('description', []) == ['Обязательное поле.']
        assert data.get('price', []) == ['Обязательное поле.']
        assert data.get('amount', []) == ['Обязательное поле.']
        assert data.get('characteristic', []) == ['Обязательное поле.']
        assert data.get('category', []) == ['Обязательное поле.']
        assert data.get('manufacturer', []) == ['Обязательное поле.']

    def test_correct_validation_unique_name(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': item.name,
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [
                {'name': char.characteristic.name, 'value': char.value}
                for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('name', None) == ['Товар с таким Название уже существует.']

    def test_correct_validation_unique_characteristic(self, client, login_admin, item):
        _, admin_access_token = login_admin

        char_list = [{'name': char.characteristic.name, 'value': char.value}
                     for char in item.itemcharacteristic_set.all()]

        data = {
            'name': 'test',
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [char for char in char_list for _ in range(2)],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('characteristics', None) == ['Характеристики не должны повторяться.']

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

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('name', None) == ['Убедитесь, что это значение содержит не более 100 символов.']
        assert data.get('description', None) == ['Убедитесь, что это значение содержит не более 1000 символов.']

    def test_correct_new_characteristic_create(self, client, login_admin, item):
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

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('characteristic', None)[0].get('id', None)

        assert Characteristic.objects.get(pk=data)

    def test_failed_negative_price_and_amount_create(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'description': 'test',
            'price': -1000,
            'amount': -1,
            'characteristic': [{'name': char.characteristic.name, 'value': char.value}
                               for char in item.itemcharacteristic_set.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('price', None) == ['Убедитесь, что это значение больше либо равно 0.']
        assert data.get('amount', None) == ['Убедитесь, что это значение больше либо равно 0.']

    def test_correct_create(self, client, login_admin, item):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'description': 'test',
            'price': 1000,
            'amount': 1,
            'characteristic': [{'id': char.id, 'name': char.name, 'value': 'test'} for char in
                               item.characteristic.all()],
            'category': item.category.id,
            'manufacturer': item.manufacturer.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        chars = [OrderedDict(char) for char in data.get('characteristic')]

        assert response.data.get('name', None) == data.get('name')
        assert response.data.get('description', None) == data.get('description')
        assert response.data.get('price', None) == data.get('price')
        assert response.data.get('characteristic', None) == chars
        assert response.data.get('category', None) == data.get('category')
        assert response.data.get('manufacturer', None) == data.get('manufacturer')
