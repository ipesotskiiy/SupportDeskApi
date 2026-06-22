from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tickets.models import (
    TicketCategory,
    Ticket,
    TicketComment,
)
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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TicketCommentViewSet(ModelViewSet):
    queryset = TicketComment.objects.select_related("author", "ticket").all()
    serializer_class = TicketCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

