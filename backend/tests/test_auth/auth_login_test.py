import json

import pytest
from rest_framework import status

from tests.factories import UserFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestAuthLoginView:
    base_url = 'auth:login'

    def test_return_correct_data_keys(self, client):
        password = 'test'

        user = UserFactory(password=password)

        initial_data = {
            'email': user.email,
            'password': password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert list(response.data.keys()) == ['refresh', 'access']
        assert len(response.data.keys()) == 2

    def test_correct_return_status_code(self, client):
        password = 'test'

        user = UserFactory(password=password)

        initial_data = {
            'email': user.email,
            'password': '1234'
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert response.data.get('detail', None) == 'Не найдено активной учетной записи с указанными данными'

        initial_data['password'] = password

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_types(self, client):
        password = 'test'

        user = UserFactory(password=password)

        initial_data = {
            'email': user.email,
            'password': password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert [type(elem) for elem in response.data.values()] == [str, str]

    def test_correct_require_field_validation(self, client):
        response = client.post(get_url(self.base_url), data={}, content_type='application/json')

        assert response.data.get('email', []) == ['Обязательное поле.']
        assert response.data.get('password', []) == ['Обязательное поле.']

    def test_correct_inactive_user_check(self, client, user):
        user.is_active = False
        user.save()

        initial_data = {
            'email': user.email,
            'password': user.password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.data.get('user', None) == ['Нужно подтвердить пользователя через электронную почту.']
