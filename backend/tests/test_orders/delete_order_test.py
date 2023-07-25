import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestDeleteOrderView:
    base_url = 'orders:delete_order'

    def test_return_correct_data_keys(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert list(data.keys()) == ['status']

    def test_correct_status_code(self, client, login_user, login_admin, order):
        _, user_access_token = login_user
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, order.id))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(get_url(self.base_url, order.id),
                                HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json().get('detail') == 'У вас недостаточно прав для выполнения данного действия.'

        response = client.patch(get_url(self.base_url, 10000), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get('detail') == 'Страница не найдена.'

        response = client.patch(get_url(self.base_url, order.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_type(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.patch(
            get_url(self.base_url, order.id), HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        data = response.data

        assert [type(elem) for elem in data.values()] == [str]

    def test_correct_item_update_activity(self, client, login_admin, order):
        _, admin_access_token = login_admin

        response = client.patch(get_url(self.base_url, order.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('status', None) == 'Отменен'

        response = client.patch(get_url(self.base_url, order.id),
                                HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')

        assert response.data.get('status', None) == ['Заказ уже отменен.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST
