import json
from collections import OrderedDict
from types import NoneType
import pytest
from rest_framework import status

from goods.models import Characteristic
from tests.utils import get_url


@pytest.mark.django_db()
class TestCreateSubCategoryView:
    base_url = 'goods:create_subcategory'

    def test_return_correct_data_keys(self, client, login_admin, category, media_root):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'category': category.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['id', 'name', 'image']

    def test_correct_status_code(self, client, login_user, login_admin, category):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'category': category.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.post(get_url(self.base_url),
                               HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'Необходимо быть администратором, чтобы выполнить данное действие.'

        response = client.post(get_url(self.base_url), data={},
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(get_url(self.base_url), data=json.dumps(data), content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client, login_admin, category):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'category': category.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [int, str, str]

    def test_correct_validation_require_field(self, client, login_admin, item):
        _, admin_access_token = login_admin

        response = client.post(
            get_url(self.base_url), data={}, content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('category', []) == ['Обязательное поле.']
        assert data.get('name', []) == ['Обязательное поле.']

    def test_correct_validation_unique_name(self, client, login_admin, category, sub_category):
        _, admin_access_token = login_admin

        data = {
            'name': sub_category.name,
            'category': category.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert data.get('name', None) == ['Подкатегория с таким Название уже существует.']

    def test_correct_create(self, client, login_admin, category):
        _, admin_access_token = login_admin

        data = {
            'name': 'test',
            'category': category.id
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('id', None)
        assert response.data.get('name', None) == data.get('name')
        assert response.data.get('image', None) == 'http://testserver/media/images/default_image.png'
