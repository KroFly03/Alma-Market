import math
from collections import OrderedDict
from types import NoneType

import pytest
from rest_framework import status

from paginations import OrderPagination
from tests.factories import OrderFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListOrderView:
    base_url = 'orders:list_order'

    def test_correct_return_pagination_keys(self, client, login_admin):
        _, admin_access_token = login_admin

        OrderFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert list(response.data.keys()) == ['links', 'count', 'total_pages', 'current_page', 'results']

    def test_correct_return_data_keys(self, client, login_admin):
        _, admin_access_token = login_admin

        OrderFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)[0]

        assert list(data.keys()) == ['id', 'goods', 'user', 'address', 'status', 'code', 'created', 'receive',
                                     'updated']
        assert list(data.get('goods', None)[0].keys()) == ['id', 'name', 'price', 'image', 'amount']
        assert list(data.get('address', None).keys()) == ['id', 'name', 'longitude', 'latitude']
        assert list(data.get('user', None).keys()) == ['first_name', 'last_name', 'phone', 'role', 'id', 'email']

    def test_correct_return_status_code(self, client, login_user, login_admin):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        OrderFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Учетные данные не были предоставлены.'

        response = client.get(get_url(self.base_url),
                              HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data.get('detail') == 'У вас недостаточно прав для выполнения данного действия.'

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_amount(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = 10

        OrderFactory.create_batch(amount)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert len(response.data.get('results', None)) == amount

    def test_correct_return_data_type(self, client, login_admin):
        _, admin_access_token = login_admin

        OrderFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)[0]

        assert [type(elem) for elem in data.values()] == [int, list, OrderedDict, OrderedDict, str, str, str, NoneType,
                                                          str]

    def test_correct_return_pagination_pages(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = 31

        OrderFactory.create_batch(amount)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('count', None) == amount
        assert response.data.get('total_pages', None) == math.ceil(amount / OrderPagination.page_size)

    def test_correct_return_pagination_links(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = 31
        page = 2

        OrderFactory.create_batch(amount)

        response = client.get(get_url(self.base_url, page=page),
                              HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('links', None) == {'previous': 'http://testserver/api/orders?page=1',
                                           'next': 'http://testserver/api/orders?page=3'}
        assert data.get('current_page', None) == page

    def test_correct_name_filter(self, client, login_admin):
        _, admin_access_token = login_admin

        orders = OrderFactory.create_batch(10)

        code = orders[0].code

        response = client.get(get_url(self.base_url, search=code),
                              HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)

        assert data[0].get('code', None) == code
        assert len(data) == 1

    def test_correct_date_ordering(self, client, login_admin):
        _, admin_access_token = login_admin

        OrderFactory.create_batch(10)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)

        assert data[0].get('created', None) > data[::-1][0].get('created', None)
