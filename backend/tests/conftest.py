import pytest

pytest_plugins = 'tests.factories'


@pytest.fixture(scope='session')
def media_root(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp('media')
    return temp_dir


@pytest.fixture()
@pytest.mark.django_db
def login_user(client, django_user_model):
    email = 'user_email'
    password = 'test_password'
    role = 'user'
    phone = 'user_phone'

    test_user = django_user_model.objects.create(email=email, password=password, role=role, phone=phone)
    test_user.is_active = True
    test_user.save()

    response = client.post('/api/auth/token/', data={"email": test_user.email, "password": password})

    return test_user, response.data.get('access')


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

    response = client.post('/api/auth/token/', data={"email": test_user.email, "password": password})

    return test_user, response.data.get('access')
