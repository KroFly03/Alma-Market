from types import NoneType

import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestDetailUserView:
    base_url = 'users:users-me'

    def test_correct_return_data_keys(self, client, login_user):
        _, user_access_token = login_user

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'last_login', 'email', 'first_name', 'last_name', 'phone', 'role',
                                     'is_active']

    def test_correct_return_status_code(self, client, login_user):
        _, user_access_token = login_user

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail') == 'Учетные данные не были предоставлены.'

        response = client.get(get_url(self.base_url),
                              HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_user):
        _, user_access_token = login_user

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, NoneType, str, str, str, str, str, bool]

    def test_correct_detail_order(self, client, login_user):
        user, user_access_token = login_user

        response = client.get(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.data.get('id', None) == user.id
