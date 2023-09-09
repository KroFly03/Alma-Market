import datetime
import json
from collections import OrderedDict
from types import NoneType
import pytest
from rest_framework import status

from orders.models import Order
from tests.utils import get_url


@pytest.mark.django_db()
class TestUpdateItemView:
    base_url = 'orders:update_order'

    def test_correct_return_data_keys(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, order.id), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'goods', 'user', 'code', 'status', 'created', 'receive', 'updated',
                                     'address']
        assert list(data.get('goods', None)[0].keys()) == ['id', 'name', 'price', 'image', 'amount']
        assert list(data.get('user', None).keys()) == ['first_name', 'last_name', 'phone', 'role', 'id', 'email']

    def test_correct_return_status_code(self, client, login_user, login_admin, order):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, order.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(get_url(self.base_url, order.id),
                                HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data.get('detail') == 'У вас недостаточно прав для выполнения данного действия.'

        response = client.patch(get_url(self.base_url, order.id),
                                content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, order.id), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert [type(elem) for elem in response.data.values()] == [int, list, OrderedDict, str, str, str, NoneType, str,
                                                                   int]

    def test_correct_status_validation(self, client, login_admin, order):
        _, admin_access_token = login_admin

        order.status = Order.Status.CANCELED
        order.save()

        response = client.patch(
            get_url(self.base_url, order.id), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('status', None) == ['Заказ уже отменен.']

    def test_correct_receive_validation(self, client, login_admin, order):
        _, admin_access_token = login_admin

        data = {
            'receive': datetime.datetime.now().isoformat()
        }

        response = client.patch(
            get_url(self.base_url, order.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('receive', None) == [
            'Дата получения должна быть позже дня создания как минимум на один день.']

    def test_correct_update(self, client, login_admin, order):
        _, admin_access_token = login_admin

        receive = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        status = Order.Status.COMPLETED

        data = {
            'receive': receive,
            'status': status,
        }

        response = client.patch(
            get_url(self.base_url, order.id), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('receive', None) == receive + 'Z'
        assert response.data.get('status', None) == status
