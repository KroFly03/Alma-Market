import json
from collections import OrderedDict
from types import NoneType
import pytest
from rest_framework import status

from goods.models import Characteristic
from orders.models import Order
from tests.utils import get_url
from users.models import Basket


@pytest.mark.django_db()
class TestCreateOrderView:
    base_url = 'orders:create_order'

    def test_return_correct_data_keys(self, client, login_admin, address, item):
        user, admin_access_token = login_admin

        Basket.objects.create(user=user, item=item, amount=1)

        data = {
            'address': address.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'goods', 'code', 'status', 'created', 'receive', 'updated', 'address']
        assert list(data.get('goods', None)[0].keys()) == ['id', 'name', 'price', 'image', 'amount']

    def test_correct_status_code(self, client, login_user, login_admin, address, item):
        _, user_access_token = login_user
        user, admin_access_token = login_admin

        Basket.objects.create(user=user, item=item, amount=1)

        data = {
            'address': address.id
        }

        response = client.post(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.post(get_url(self.base_url), data={},
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client, login_admin, item, address):
        user, admin_access_token = login_admin

        Basket.objects.create(user=user, item=item, amount=1)

        data = {
            'address': address.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, list, str, str, str, NoneType, str, int]

    def test_correct_validation_require_field(self, client, login_admin):
        _, admin_access_token = login_admin

        response = client.post(
            get_url(self.base_url), data={}, content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('address', []) == ['Обязательное поле.']

    def test_correct_validation_empty_basket(self, client, login_admin, address):
        user, admin_access_token = login_admin

        data = {
            'address': address.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.json().get('goods') == ['В корзине отсутствуют товары.']

    def test_correct_validation_item_amount(self, client, login_admin, item, address):
        user, admin_access_token = login_admin
        amount = item.amount * 2

        Basket.objects.create(user=user, item=item, amount=amount)

        data = {
            'address': address.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.json().get(item.name) == [f'Данного товара в количестве {amount} шт. нет в наличии']

    def test_correct_create(self, client, login_admin, item, address):
        user, admin_access_token = login_admin
        amount = 1
        address = address.id

        Basket.objects.create(user=user, item=item, amount=amount)

        data = {
            'address': address
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        goods = [OrderedDict(
            {'id': item.id, 'name': item.name, 'price': item.price,
             'image': 'http://testserver/media/images/default_image.png', 'amount': amount})]
        print(response.data)
        assert response.data.get('goods', None) == goods
        assert response.data.get('code', None)
        assert response.data.get('status', None) == Order.Status.FORMED
        assert response.data.get('created', None)
        assert not response.data.get('receive', None)
        assert response.data.get('updated', None)
        assert response.data.get('address', None) == address
