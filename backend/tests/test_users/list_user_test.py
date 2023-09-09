import math
from types import NoneType

import pytest
from rest_framework import status

from paginations import UserPagination
from tests.factories import UserFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListUserView:
    base_url = 'users:users-list'

    def test_correct_return_pagination_keys(self, client, login_admin):
        _, admin_access_token = login_admin

        UserFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert list(response.data.keys()) == ['links', 'count', 'total_pages', 'current_page', 'results']

    def test_correct_return_data_keys(self, client, login_admin):
        _, admin_access_token = login_admin

        UserFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)[0]

        assert list(data.keys()) == ['id', 'last_login', 'email', 'first_name', 'last_name', 'phone', 'role',
                                     'is_active']

    def test_correct_return_status_code(self, client, login_user, login_admin):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        UserFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Учетные данные не были предоставлены.'

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_amount(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = UserPagination.page_size

        UserFactory.create_batch(amount)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert len(response.data.get('results', None)) == amount

    def test_correct_return_data_type(self, client, login_admin):
        _, admin_access_token = login_admin

        UserFactory.create_batch(5)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)[0]

        assert [type(elem) for elem in data.values()] == [int, NoneType, str, str, str, str, str, bool]

    def test_correct_return_pagination_pages(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = 17

        UserFactory.create_batch(amount)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('count', None) == amount + 1
        assert response.data.get('total_pages', None) == math.ceil(amount / UserPagination.page_size)

    def test_correct_return_pagination_links(self, client, login_admin):
        _, admin_access_token = login_admin

        amount = 33
        page = 2

        UserFactory.create_batch(amount)

        response = client.get(get_url(self.base_url, page=page),
                              HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('links', None) == {'previous': 'http://testserver/api/users?page=1',
                                           'next': 'http://testserver/api/users?page=3'}
        assert data.get('current_page', None) == page

    def test_correct_first_name_filter(self, client, login_admin):
        _, admin_access_token = login_admin

        users = UserFactory.create_batch(10)

        first_name = users[0].first_name

        response = client.get(get_url(self.base_url, search=first_name),
                              HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)

        assert data[0].get('first_name', None) == first_name
        assert len(data) == 1

    def test_correct_last_name_filter(self, client, login_admin):
        _, admin_access_token = login_admin

        users = UserFactory.create_batch(10)

        last_name = users[0].last_name

        response = client.get(get_url(self.base_url, search=last_name),
                              HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)

        assert data[0].get('last_name', None) == last_name
        assert len(data) == 1

    def test_correct_id_ordering(self, client, login_admin):
        _, admin_access_token = login_admin

        UserFactory.create_batch(10)

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data.get('results', None)

        assert data[0].get('id', None) < data[::-1][0].get('id', None)
