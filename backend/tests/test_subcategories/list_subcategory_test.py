import pytest
from rest_framework import status

from tests.factories import SubCategoryFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListSubCategoryView:
    base_url = 'goods:list_subcategory'

    def test_return_correct_data_keys(self, client):
        SubCategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert list(response.data[0].keys()) == ['id', 'name', 'image']

    def test_correct_status_code(self, client):
        SubCategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_amount(self, client):
        amount = 20

        SubCategoryFactory.create_batch(20)

        response = client.get(get_url(self.base_url))

        assert len(response.data) == amount

    def test_correct_data_type(self, client):
        SubCategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data[0]

        assert [type(elem) for elem in data.values()] == [int, str, str]
