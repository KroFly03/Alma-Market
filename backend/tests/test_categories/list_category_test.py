import pytest
from rest_framework import status

from tests.factories import CategoryFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListCategoryView:
    base_url = 'goods:list_category'
    
    def test_return_correct_data_keys(self, client):
        CategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data[0]

        assert list(data.keys()) == ['id', 'total_goods', 'subcategory', 'name']
        assert list(data.get('subcategory')[0].keys()) == ['id', 'name']

    def test_correct_status_code(self, client):
        CategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_amount(self, client):
        amount = 20

        CategoryFactory.create_batch(20)

        response = client.get(get_url(self.base_url))

        assert len(response.data) == amount

    def test_correct_data_type(self, client):
        CategoryFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data[0]

        assert [type(elem) for elem in data.values()] == [int, int, list, str]

    def test_correct_name_filter(self, client):
        categories = CategoryFactory.create_batch(10)

        name = categories[0].name

        response = client.get(get_url(self.base_url, search=name))

        data = response.data

        assert data[0].get('name', None) == name
        assert len(data) == 1
