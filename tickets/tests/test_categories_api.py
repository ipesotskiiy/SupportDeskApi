import pytest
from rest_framework import status

from tickets.models import TicketCategory

pytestmark = pytest.mark.django_db

def test_error_categories_unauthorize_user(api_client):
    response = api_client.get("/api/categories/")

    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


def test_success_categories_authorize_user(
        authenticated_client,
        ticket_category,
):
    response = authenticated_client.get("/api/categories/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results") is not None
    assert len(response.data["results"]) >= 1


def test_authorize_user_create_category(
        authenticated_client,
        ticket_category,
):
    count_categories = TicketCategory.objects.count()

    name_for_category = "Debug"
    slug_for_category = "debug"
    response = authenticated_client.post(
        r"/api/categories/",
        data={
            "name": name_for_category,
            "slug": slug_for_category,
            "description": "test_cat"
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert count_categories < TicketCategory.objects.count()
    assert name_for_category == response.data["name"]
    assert slug_for_category == response.data["slug"]
