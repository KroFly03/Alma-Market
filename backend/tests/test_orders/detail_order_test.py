from collections import OrderedDict
from types import NoneType

import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestDetailOrderView:
    base_url = 'orders:detail_order'

    def test_return_correct_data_keys(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.get(get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'goods', 'user', 'address', 'status', 'code', 'created', 'receive',
                                     'updated']
        assert list(data.get('goods', None)[0].keys()) == ['id', 'name', 'price', 'image', 'amount']
        assert list(data.get('address', None).keys()) == ['id', 'name']
        assert list(data.get('user', None).keys()) == ['first_name', 'last_name', 'phone', 'role', 'id', 'email']

    def test_correct_status_code(self, client, login_user, login_admin, order):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        response = client.get(get_url(self.base_url, order.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.get(get_url(self.base_url, order.id),
                              HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'У вас недостаточно прав для выполнения данного действия.'

        response = client.get(get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_type(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.get(get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, list, OrderedDict, OrderedDict, str, str, str, NoneType,
                                                          str]

    def test_correct_detail_order(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.get(get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('id', None) == order.id
