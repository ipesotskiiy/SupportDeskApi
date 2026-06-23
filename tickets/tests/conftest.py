import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tickets.models import TicketCategory, Ticket, TicketStatus

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user_model = get_user_model()
    user_obj = user_model.objects.create_user(
        username="no_staff_user",
        email="test@mail.com",
        password="fusiontech",
    )
    return user_obj


@pytest.fixture
def second_user():
    user_model = get_user_model()
    second_user_obj = user_model.objects.create_user(
        username="second_no_staff_user",
        email="second_test@mail.com",
        password="fusiontech2",
    )
    return second_user_obj


@pytest.fixture
def staff_user():
    user_model = get_user_model()
    staff_user_obj = user_model.objects.create_user(
        username="staff_user",
        email="test_staff@mail.com",
        password="fusiontech1",
        is_staff=True,
    )
    return staff_user_obj


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def second_authenticated_client(api_client, second_user):
    api_client.force_authenticate(user=second_user)
    return api_client


@pytest.fixture
def staff_authenticated_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client


@pytest.fixture
def ticket_category():
    return TicketCategory.objects.create(
        name="Authentication",
        slug="authentication",
        description="Login, password and account access problems",
    )


@pytest.fixture
def user_ticket(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 2",
        description="User cannot login after password reset",
        priority="high",
    )


@pytest.fixture
def second_user_ticket(second_user, ticket_category):
    return Ticket.objects.create(
        author=second_user,
        category=ticket_category,
        title="Cannot login 3",
        description="Second user cannot login after password reset",
        priority="high",
    )


@pytest.fixture
def closed_user_ticket(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 4",
        description="Closed user cannot login after password reset",
        priority="high",
        status=TicketStatus.CLOSED,
        closed_at=timezone.now()
    )
