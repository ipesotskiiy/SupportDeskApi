import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db

def test_cannot_see_tickets_another_author(
        authenticated_client,
        user_ticket,
        second_user_ticket,
):
    response = authenticated_client.get("/api/tickets/")
    response_ticket_ids = {
        ticket_data["id"]
        for ticket_data in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert response_ticket_ids == {user_ticket.id}
    assert second_user_ticket.id not in response_ticket_ids


def test_error_get_another_author_ticket(authenticated_client, second_user_ticket):
    response = authenticated_client.get(f"/api/tickets/{second_user_ticket.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_error_change_another_author_ticket(authenticated_client, second_user_ticket):
    response = authenticated_client.patch(
        f"/api/tickets/{second_user_ticket.id}/",
        data={"description": "Hacked description"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_get_all_tickets(
        staff_authenticated_client,
        user_ticket,
        second_user_ticket,
):
    response = staff_authenticated_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2

    response_ticket_ids = {
        ticket_data["id"]
        for ticket_data in response.data["results"]
    }

    assert response_ticket_ids == {user_ticket.id, second_user_ticket.id}


def test_staff_change_another_author_ticket(staff_authenticated_client, user_ticket):
    new_description = "Changed by staff"
    response = staff_authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
          "description": new_description
        },
        format="json",
    )
    user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user_ticket.description == new_description
