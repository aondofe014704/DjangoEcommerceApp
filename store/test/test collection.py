from rest_framework import status
from rest_framework.test import APIClient


class TestCollection:
    def test_that_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/store/collections/', {"title": "ecommerce"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
