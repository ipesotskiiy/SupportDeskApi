from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tickets.models import (
    TicketCategory,
    Ticket,
    TicketComment,
)
from tickets.permissions import IsOwnerOrStaff
from tickets.serializers import (
    TicketCategorySerializer,
    TicketSerializer,
    TicketCommentSerializer,
)


# Create your views here.
class TicketCategoryViewSet(ModelViewSet):
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("name", "slug")
    search_fields = (
        "name",
        "slug",
        "description",
    )
    ordering_fields = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    ordering = ("name",)


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.select_related("author", "category").all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaff)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        "status",
        "priority",
        "category",
    )
    search_fields = (
        "title",
        "description",
        "author__username",
        "category__name",
    )
    ordering_fields = (
        "id",
        "title",
        "status",
        "priority",
        "created_at",
        "updated_at",
        "closed_at",
    )
    ordering = ("-created_at",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Ticket.objects.select_related("author", "category").all()
        else:
            queryset = Ticket.objects.select_related("author", "category").filter(author=self.request.user)

        return queryset


class TicketCommentViewSet(ModelViewSet):
    queryset = TicketComment.objects.select_related("author", "ticket").all()
    serializer_class = TicketCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaff)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("ticket",)
    search_fields = (
        "text",
        "author__username",
        "ticket__title",
    )
    ordering_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("created_at",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = TicketComment.objects.select_related("author", "ticket").all()
        else:
            queryset = TicketComment.objects.select_related("author", "ticket").filter(author=self.request.user)

        return queryset

