import pytest

from tests.utils import get_url
from users.models import Basket

pytest_plugins = 'tests.factories'

auth_url = get_url('auth:login')


@pytest.fixture()
@pytest.mark.django_db
def login_user(client, django_user_model, item):
    email = 'user_email'
    password = 'test_password'
    role = 'user'
    phone = 'user_phone'

    test_user = django_user_model.objects.create(email=email, password=password, role=role, phone=phone)
    test_user.is_active = True
    test_user.save()

    Basket.objects.create(user=test_user, item=item, amount=1)

    response = client.post(auth_url, data={"email": test_user.email, "password": password})

    return test_user, response.data.get('access')


@pytest.fixture()
@pytest.mark.django_db
def refresh_user(client, django_user_model):
    email = 'user_email'
    password = 'test_password'
    role = 'user'
    phone = 'user_phone'

    test_user = django_user_model.objects.create(email=email, password=password, role=role, phone=phone)
    test_user.is_active = True
    test_user.save()

    response = client.post(auth_url, data={"email": test_user.email, "password": password})

    return test_user, response.data.get('refresh')


@pytest.fixture()
@pytest.mark.django_db
def login_admin(client, django_user_model):
    email = 'admin_email'
    password = 'test_password'
    role = 'admin'
    phone = 'admin_phone'

    test_user = django_user_model.objects.create(email=email, password=password, role=role, phone=phone)
    test_user.is_active = True
    test_user.save()

    response = client.post(auth_url, data={"email": test_user.email, "password": password})

    return test_user, response.data.get('access')
