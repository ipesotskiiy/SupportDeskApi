import pytest
from rest_framework import status

from tickets.models import (
    TicketStatus,
    Ticket,
    TicketPriority,
    TicketComment,
)

pytestmark = pytest.mark.django_db

def test_filter_status(
    authenticated_client,
    user_ticket,
    closed_user_ticket,
    in_progress_user_ticket,
):
    response = authenticated_client.get("/api/tickets/?status=closed")

    response_ticket_statuses = {
        ticket["status"]
        for ticket in response.data["results"]
    }

    response_ticket_ids = {
        ticket["id"]
        for ticket in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert TicketStatus.CLOSED in response_ticket_statuses
    assert TicketStatus.OPEN not in response_ticket_statuses
    assert TicketStatus.IN_PROGRESS not in response_ticket_statuses
    assert response_ticket_ids == {closed_user_ticket.id}


def test_filter_priority(
    user,
    ticket_category,
    in_progress_user_ticket,
    authenticated_client,
):
    Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Alpha issue",
        description="First ticket for ordering test",
        priority=TicketPriority.LOW,
        status=TicketStatus.OPEN,
    )

    Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Zulu issue",
        description="Second ticket for ordering test",
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
    )

    response = authenticated_client.get("/api/tickets/?priority=high")

    response_ticket_priorities = {
        ticket["priority"]
        for ticket in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert TicketPriority.HIGH in response_ticket_priorities
    assert TicketPriority.MEDIUM not in response_ticket_priorities
    assert TicketPriority.LOW not in response_ticket_priorities


def test_filter_category(
    authenticated_client,
    user_ticket,
    payment_ticket,
    payment_category,
    ticket_category,
    user,
):

    response = authenticated_client.get(f"/api/tickets/?category={payment_category.id}")
    response_ticket_categories = {
        ticket["category"]
        for ticket in response.data["results"]
    }
    response_ticket_ids = {
        ticket["id"]
        for ticket in response.data["results"]
    }


    assert response.status_code == status.HTTP_200_OK
    assert payment_category.id in response_ticket_categories
    assert ticket_category.id not in response_ticket_categories
    assert response_ticket_ids == {payment_ticket.id}


def test_title_search(
    authenticated_client,
    user_ticket,
    payment_ticket,
):
    response = authenticated_client.get("/api/tickets/?search=login")

    ticket_titles = {
        ticket["title"]
        for ticket in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert user_ticket.title in ticket_titles
    assert payment_ticket.title not in ticket_titles


def test_ordering_title(
    authenticated_client,
    user,
    payment_category,
):
    alpha_ticket = Ticket.objects.create(
        author=user,
        category=payment_category,
        title="Alpha issue",
        description="Billing system created duplicate transaction",
        priority=TicketPriority.MEDIUM,
    )
    zulu_ticket = Ticket.objects.create(
        author=user,
        category=payment_category,
        title="Zulu issue",
        description="Billing system created duplicate transaction",
        priority=TicketPriority.MEDIUM,
    )

    response = authenticated_client.get("/api/tickets/?ordering=title")
    tickets_titles = [ticket["title"] for ticket in response.data["results"]]

    assert response.status_code == status.HTTP_200_OK
    assert tickets_titles.index(alpha_ticket.title) < tickets_titles.index(zulu_ticket.title)

    response = authenticated_client.get("/api/tickets/?ordering=-title")
    tickets_titles = [ticket["title"] for ticket in response.data["results"]]

    assert response.status_code == status.HTTP_200_OK
    assert tickets_titles.index(alpha_ticket.title) > tickets_titles.index(zulu_ticket.title)


def test_search_comments(
        authenticated_client,
        user,
        user_ticket,
):
    invoice_comment = TicketComment.objects.create(
        ticket=user_ticket,
        author=user,
        text="Invoice problem reproduced",
    )

    login_comment = TicketComment.objects.create(
        ticket=user_ticket,
        author=user,
        text="Login problem reproduced",
    )

    response = authenticated_client.get("/api/comments/?search=invoice")
    comments_text = {comment["text"] for comment in response.data["results"]}

    assert response.status_code == status.HTTP_200_OK
    assert invoice_comment.text in comments_text
    assert login_comment.text not in comments_text




