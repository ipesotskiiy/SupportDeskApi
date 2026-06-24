import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_pagination(
    authenticated_client,
    user,
    user_ticket,
    user_ticket_medium_priority,
    user_ticket_low_priority,
    payment_ticket,
    closed_user_ticket,
    in_progress_user_ticket
):
    response = authenticated_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK
    assert "count" in response.data
    assert "next" in response.data
    assert "previous" in response.data
    assert "results" in response.data
    assert response.data["count"] == 6
    assert len(response.data["results"]) == 5
    assert response.data["next"] is not None
    assert response.data["previous"] is None



def test_pagination_second_page(
    authenticated_client,
    user,
    user_ticket,
    user_ticket_medium_priority,
    user_ticket_low_priority,
    payment_ticket,
    closed_user_ticket,
    in_progress_user_ticket
):
    response = authenticated_client.get("/api/tickets/?page=2")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 6
    assert len(response.data["results"]) == 1
    assert response.data["previous"] is not None
    assert response.data["next"] is None
