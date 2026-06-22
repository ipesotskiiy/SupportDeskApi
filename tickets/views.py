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


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.select_related("author", "category").all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaff)

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = TicketComment.objects.select_related("author", "ticket").all()
        else:
            queryset = TicketComment.objects.select_related("author", "ticket").filter(author=self.request.user)

        return queryset

