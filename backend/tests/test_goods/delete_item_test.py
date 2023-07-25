import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestDeleteItemView:
    base_url = 'goods:delete_item'
    
    def test_return_correct_data_keys(self, client, login_admin, item):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, item.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['is_active']

    def test_correct_status_code(self, client, login_user, login_admin, item):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, item.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(get_url(self.base_url, item.id),
                                HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'У вас недостаточно прав для выполнения данного действия.'

        response = client.patch(get_url(self.base_url, 10000), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get('detail') == 'Страница не найдена.'

        response = client.patch(get_url(self.base_url, item.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_admin, item):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, item.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [bool]

    def test_correct_item_update_activity(self, client, login_admin, item):
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, item.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert not response.data.get('is_active', None)

        response = client.patch(get_url(self.base_url, item.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('item', None) == ['Данный товар помечен как неактивный.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST
