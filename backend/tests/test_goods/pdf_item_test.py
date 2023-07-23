import pytest
from rest_framework import status

from tests.utils import get_url


@pytest.mark.django_db()
class TestPDFItemView:
    base_url = 'goods:pdf_list_item'
    
    def test_return_correct_status_code(self, client):
        response = client.post(get_url(self.base_url))

        assert response.status_code == status.HTTP_200_OK
        assert response.get('Content-Type') == 'application/pdf'
