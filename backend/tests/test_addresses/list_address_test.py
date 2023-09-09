import pytest
from rest_framework import status

from tests.factories import AddressFactory
from tests.utils import get_url


@pytest.mark.django_db()
class TestListAddressView:
    base_url = 'orders:list_address'
    
    def test_correct_return_data_keys(self, client):
        AddressFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data[0]

        assert list(data.keys()) == ['id', 'name', 'longitude', 'latitude']
        assert len(data.keys()) == 4

    def test_correct_return_status_code(self, client):
        AddressFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        assert response.status_code == status.HTTP_200_OK

    def test_correct_return_data_amount(self, client):
        amount = 20

        AddressFactory.create_batch(20)

        response = client.get(get_url(self.base_url))

        assert len(response.data) == amount

    def test_correct_data_type(self, client):
        AddressFactory.create_batch(5)

        response = client.get(get_url(self.base_url))

        data = response.data[0]

        assert [type(field) for field in data.values()] == [int, str, float, float]

    def test_correct_name_filter(self, client):
        addresses = AddressFactory.create_batch(10)

        name = addresses[0].name

        response = client.get(get_url(self.base_url, search=name))

        assert response.data[0].get('name', None) == name
        assert len(response.data) == 1
