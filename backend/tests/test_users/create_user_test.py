import json
from collections import OrderedDict
from types import NoneType
import pytest
from rest_framework import status

from goods.models import Characteristic
from orders.models import Order
from tests.utils import get_url
from users.models import Basket


@pytest.mark.django_db()
class TestCreateCreateView:
    base_url = 'users:users-list'

    def test_return_correct_data_keys(self, client):
        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        data = response.data

        assert list(data.keys()) == ['id', 'email', 'first_name', 'last_name', 'phone']

    def test_correct_status_code(self, client):
        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client):
        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert [type(elem) for elem in response.data.values()] == [int, str, str, str, str]

    def test_correct_validation_require_field(self, client):
        response = client.post(
            get_url(self.base_url), data={}, content_type='application/json')

        data = response.data

        assert data.get('email', []) == ['Обязательное поле.']
        assert data.get('last_name', []) == ['Обязательное поле.']
        assert data.get('first_name', []) == ['Обязательное поле.']
        assert data.get('phone', []) == ['Обязательное поле.']
        assert data.get('password', []) == ['Обязательное поле.']
        assert data.get('password_repeat', []) == ['Обязательное поле.']

    def test_correct_data_validation(self, client, user):
        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+799988877665',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.json().get('phone') == ['Номер телефона должен быть в формате: "+79991234567".']

        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.json().get('password') == ['Разные пароли.']

        data = {
            'email': 'test',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': 'test',
            'password_repeat': 'test',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')
        print(response.data)
        assert response.json().get('email') == ['Введите правильный адрес электронной почты.']
        assert response.json().get('password') == [
            'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.',
            'Введённый пароль слишком широко распространён.']

        data = {
            'email': user.email,
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.json().get('email') == ['Пользователь с таким email уже существует.']

    def test_correct_create(self, client):
        data = {
            'email': 'test@mail.ru',
            'last_name': 'test',
            'first_name': 'test',
            'phone': '+79998887766',
            'password': '1qa2ws3ed4rf5tg',
            'password_repeat': '1qa2ws3ed4rf5tg',
        }

        response = client.post(
            get_url(self.base_url), data=json.dumps(data), content_type='application/json')

        assert response.data.get('id', None)
        assert response.data.get('email', None) == data.get('email')
        assert response.data.get('last_name', None) == data.get('last_name')
        assert response.data.get('first_name', None) == data.get('first_name')
        assert response.data.get('phone', None) == data.get('phone')
