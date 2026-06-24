import pytest
from rest_framework import status

from tickets.models import TicketComment


pytestmark = pytest.mark.django_db

def test_comment_user_ticket(
    authenticated_client,
    user_ticket,
    user,
):
    response = authenticated_client.post(
        "/api/comments/",
        data={
          "ticket": f"{user_ticket.id}",
          "text": "User comment text"
        },
        format="json",
    )

    comment = TicketComment.objects.get(id=response.data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert comment.author == user
    assert comment.ticket == user_ticket


def test_error_user_comment_ticket_another_author(authenticated_client, second_user_ticket):
    response = authenticated_client.post(
        "/api/comments/",
        data={
            "ticket": f"{second_user_ticket.id}",
            "text": "Trying to comment another user's ticket"
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_staff_commet_another_ticket_author(
    staff_authenticated_client,
    user_ticket,
    staff_user,
):
    response = staff_authenticated_client.post(
        "/api/comments/",
        data={
            "ticket": f"{user_ticket.id}",
            "text": "Staff comment"
        },
        format="json",
    )
    comment = TicketComment.objects.get(id=response.data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert comment.author == staff_user
    assert comment.ticket == user_ticket


def test_user_cant_comment_closed_ticket(authenticated_client, closed_user_ticket):
    response = authenticated_client.post(
        "/api/comments/",
        data={
            "ticket": f"{closed_user_ticket.id}",
            "text": "Trying to comment closed ticket"
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_staff_comment_closed_ticket(
        staff_authenticated_client,
        closed_user_ticket,
        staff_user,
):
    response = staff_authenticated_client.post(
        "/api/comments/",
        data={
            "ticket": f"{closed_user_ticket.id}",
            "text": "Staff comment on closed ticket"
        },
        format="json",
    )
    comment = TicketComment.objects.get(id=response.data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert comment.author == staff_user
    assert comment.ticket == closed_user_ticket


def test_user_see_only_his_comments(
    authenticated_client,
    user_comment,
    second_user_comment,
):
    response = authenticated_client.get("/api/comments/")

    response_comments_ids = {
        comment_data["id"]
        for comment_data in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert user_comment.id in response_comments_ids
    assert second_user_comment.id not in response_comments_ids


def test_staff_see_all_comments(
    staff_authenticated_client,
    user_comment,
    second_user_comment
):
    response = staff_authenticated_client.get("/api/comments/")
    response_comment_ids = {
        comment_data["id"]
        for comment_data in response.data["results"]
    }

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2
    assert response_comment_ids == {user_comment.id, second_user_comment.id}


