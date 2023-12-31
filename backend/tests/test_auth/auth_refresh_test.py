import json

import pytest
from rest_framework import status


from tests.utils import get_url


@pytest.mark.django_db()
class TestAuthRefreshView:
    base_url = 'auth:refresh'

    def test_return_correct_data_keys(self, client, refresh_user):
        _, user_refresh_token = refresh_user

        initial_data = {
            'refresh': user_refresh_token
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert list(response.data.keys()) == ['access', 'refresh']
        assert len(response.data.keys()) == 2

    def test_correct_return_status_code(self, client, refresh_user):
        _, user_refresh_token = refresh_user

        initial_data = {
            'refresh': 'test',
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail', None) == 'Токен недействителен или просрочен'

        initial_data['refresh'] = user_refresh_token

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_types(self, client, refresh_user):
        _, user_refresh_token = refresh_user

        initial_data = {
            'refresh': user_refresh_token
        }

        response = client.post(get_url(self.base_url), data=json.dumps(initial_data), content_type='application/json')

        assert [type(elem) for elem in response.data.values()] == [str, str]

    def test_correct_require_field_validation(self, client):
        response = client.post(get_url(self.base_url), data={'qwe': 'qwe'}, content_type='application/json')

        assert response.data.get('refresh', []) == ['Обязательное поле.']
