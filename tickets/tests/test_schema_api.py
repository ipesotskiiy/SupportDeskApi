import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_schema_is_available(api_client):
    response = api_client.get("/api/schema/")

    assert response.status_code == status.HTTP_200_OK


def test_swagger_ui_is_available(api_client):
    response = api_client.get("/api/docs/")

    assert response.status_code == status.HTTP_200_OK


def test_redoc_is_available(api_client):
    response = api_client.get("/api/redoc/")

    assert response.status_code == status.HTTP_200_OK