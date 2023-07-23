import json

import pytest
from rest_framework import status

from tests.factories import SubCategoryFactory, UserFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestAuthLoginView:
    base_url = 'users:login'

    def test_return_correct_data_keys(self, client):
        password = 'test'

        user = UserFactory(password=password)

        data = {
            'email': user.email,
            'password': password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert list(response.data.keys()) == ['refresh', 'access']

    def test_correct_status_code(self, client):
        password = 'test'

        user = UserFactory(password=password)

        data = {
            'email': user.email,
            'password': '1234'
        }

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail', None) == 'Не найдено активной учетной записи с указанными данными'

        data = {
            'email': user.email,
            'password': password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_types(self, client):
        password = 'test'

        user = UserFactory(password=password)

        data = {
            'email': user.email,
            'password': password
        }

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert [type(elem) for elem in response.data.values()] == [str, str]

    def test_correct_validation_require_field(self, client):
        response = client.post(get_url(self.base_url), data={'qwe': 'qwe'}, content_type='application/json')

        assert response.data.get('email', []) == ['Обязательное поле.']
        assert response.data.get('password', []) == ['Обязательное поле.']
