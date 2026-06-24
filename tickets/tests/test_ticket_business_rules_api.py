import pytest
from rest_framework import status

from tickets.models import TicketStatus


pytestmark = pytest.mark.django_db

def test_user_cannot_change_ticket_status(authenticated_client, user_ticket):
    response = authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
          "status": "in_progress"
        },
        format="json",
    )
    user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user_ticket.status == TicketStatus.OPEN


def test_user_cannot_close_ticket(authenticated_client, user_ticket):
    response = authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
            "status": "closed"
        },
        format="json",
    )
    user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user_ticket.status == TicketStatus.OPEN
    assert user_ticket.closed_at is None


def test_staff_close_ticket(staff_authenticated_client, user_ticket):
    response = staff_authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
            "status": "closed"
        },
        format="json",
    )
    user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user_ticket.status == TicketStatus.CLOSED
    assert user_ticket.closed_at is not None


def test_staff_open_closed_ticket(staff_authenticated_client, user_ticket):
    staff_authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
            "status": "closed"
        },
        format="json",
    )
    user_ticket.refresh_from_db()

    response = staff_authenticated_client.patch(
        f"/api/tickets/{user_ticket.id}/",
        data={
            "status": "open"
        },
        format="json",
    )

    user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user_ticket.status == TicketStatus.OPEN
    assert user_ticket.closed_at is None


def test_user_not_change_closed_ticket(authenticated_client, closed_user_ticket):
    ticket_description = closed_user_ticket.description

    response = authenticated_client.patch(
        f"/api/tickets/{closed_user_ticket.id}/",
        data={
          "description": "Trying to edit closed ticket"
        },
        format="json",
    )
    closed_user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert closed_user_ticket.description == ticket_description


def test_staff_change_closed_ticket(staff_authenticated_client, closed_user_ticket):
    new_ticket_description = "Changed closed ticket by staff"
    response = staff_authenticated_client.patch(
        f"/api/tickets/{closed_user_ticket.id}/",
        data={
            "description": "Changed closed ticket by staff"
        },
        format="json",
    )
    closed_user_ticket.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert closed_user_ticket.description == new_ticket_description
