import pytest
from rest_framework import status

from tickets.models import Ticket, TicketStatus

pytestmark = pytest.mark.django_db

def test_error_tickets_unauthorize_user(api_client):
    response = api_client.get("/api/tickets/")

    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


def test_create_ticket_authorize_user(
    user,
    authenticated_client,
    ticket_category,
):
    response = authenticated_client.post(
        "/api/tickets/",
        data={
            "category": ticket_category.id,
            "title": "Cannot login",
            "description": "User cannot login after password reset",
            "priority": "high",
        },
        format="json",
    )
    ticket = Ticket.objects.get(id=response.data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert Ticket.objects.count() == 1
    assert ticket.author == user
    assert ticket.status == TicketStatus.OPEN
    assert ticket.closed_at is None


def test_no_staff_user_watch_only_him_tickets(
    user,
    staff_user,
    authenticated_client,
    ticket_category,
):
    user_ticket = Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login",
        description="User cannot login after password reset",
        priority="high",
    )

    Ticket.objects.create(
        author=staff_user,
        category=ticket_category,
        title="Staff cannot login",
        description="Staff user cannot login after password reset",
        priority="high",
    )

    response = authenticated_client.get("/api/tickets/")
    ticket_response_obj = Ticket.objects.get(id=response.data['results'][0]['id'])

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert ticket_response_obj == user_ticket


def test_staff_user_watch_all_tickets(
    user,
    staff_user,
    staff_authenticated_client,
    ticket_category,
):
    first_ticket = Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login",
        description="User cannot login after password reset",
        priority="high",
    )

    second_ticket = Ticket.objects.create(
        author=staff_user,
        category=ticket_category,
        title="Staff cannot login",
        description="Staff user cannot login after password reset",
        priority="high",
    )

    response = staff_authenticated_client.get("/api/tickets/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2

    response_ticket_ids = {
        ticket_data["id"]
        for ticket_data in response.data["results"]
    }

    assert response_ticket_ids == {first_ticket.id, second_ticket.id}