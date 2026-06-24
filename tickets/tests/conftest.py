import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tickets.models import (
    TicketCategory,
    Ticket,
    TicketStatus,
    TicketComment,
    TicketPriority,
)


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


@pytest.fixture()
def payment_category():
    return TicketCategory.objects.create(
        name="Payments",
        slug="payments",
        description="Billing, invoices, refunds and payment processing problems",
    )


@pytest.fixture
def user_ticket(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 2",
        description="User cannot login after password reset",
        priority=TicketPriority.HIGH,
    )


@pytest.fixture
def user_ticket_medium_priority(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 2",
        description="User cannot login after password reset",
        priority=TicketPriority.MEDIUM,
    )


@pytest.fixture
def user_ticket_low_priority(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 2",
        description="User cannot login after password reset",
        priority=TicketPriority.LOW,
    )


@pytest.fixture
def payment_ticket(user, payment_category):
    return Ticket.objects.create(
        author=user,
        category=payment_category,
        title="Payment was charged twice",
        description="Billing system created duplicate transaction",
        priority=TicketPriority.MEDIUM,
    )


@pytest.fixture
def second_user_ticket(second_user, ticket_category):
    return Ticket.objects.create(
        author=second_user,
        category=ticket_category,
        title="Cannot login 3",
        description="Second user cannot login after password reset",
        priority=TicketPriority.HIGH,
    )


@pytest.fixture
def closed_user_ticket(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Cannot login 4",
        description="Closed user cannot login after password reset",
        priority=TicketPriority.HIGH,
        status=TicketStatus.CLOSED,
        closed_at=timezone.now(),
    )


@pytest.fixture
def in_progress_user_ticket(user, ticket_category):
    return Ticket.objects.create(
        author=user,
        category=ticket_category,
        title="Invoice generation is delayed",
        description="Customer invoice is still being processed",
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.IN_PROGRESS,
    )


@pytest.fixture
def user_comment(user, user_ticket):
    return TicketComment.objects.create(
        ticket=user_ticket,
        author=user,
        text="User added more details about the login problem",
    )


@pytest.fixture
def second_user_comment(second_user, second_user_ticket):
    return TicketComment.objects.create(
        ticket=second_user_ticket,
        author=second_user,
        text="Second user reported a payment confirmation issue",
    )
