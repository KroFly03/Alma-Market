import datetime
import json
from types import NoneType

import pytest
from rest_framework import status

from orders.models import Order
from tests.utils import get_url


@pytest.mark.django_db()
class TestUpdateUserView:
    base_url = 'users:users-me'

    def test_return_correct_data_keys(self, client, login_user):
        _, user_access_token = login_user

        response = client.patch(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'last_login', 'email', 'first_name', 'last_name', 'phone', 'role',
                                     'is_active']

    def test_correct_status_code(self, client, login_user):
        _, user_access_token = login_user

        response = client.patch(get_url(self.base_url))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(get_url(self.base_url),
                                HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_type(self, client, login_user):
        _, user_access_token = login_user

        response = client.patch(get_url(self.base_url), HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, NoneType, str, str, str, str, str, bool]

    def test_correct_read_only_fields(self, client, login_user):
        user, user_access_token = login_user

        data = {
            'id': 100,
            'email': 'test@mail.ru',
            'role': 'admin',
            'is_active': False,
            'last_login': datetime.datetime.now().isoformat()
        }

        response = client.patch(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.data.get('id', None) == user.id
        assert response.data.get('email', None) == user.email
        assert response.data.get('role', None) == user.role
        assert response.data.get('is_active', None) == user.is_active
        assert response.data.get('last_login', None) == user.last_login

    def test_correct_number_validation(self, client, login_user):
        user, user_access_token = login_user

        data = {
            'phone': "test"
        }

        response = client.patch(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.json().get('phone', None) == ['Номер телефона должен быть в формате: "+79991234567".']

    def test_correct_update(self, client, login_user):
        _, user_access_token = login_user

        initial_data = {
            'first_name': 'test',
            'last_name': 'test',
            'phone': '+79998887766'
        }

        response = client.patch(
            get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        data = response.data
        print(data)
        assert data.get('first_name', None) == initial_data.get('first_name')
        assert data.get('last_name', None) == initial_data.get('last_name')
        assert data.get('phone', None) == initial_data.get('phone')
