from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tickets.views import (
    TicketCategoryViewSet,
    TicketViewSet,
    TicketCommentViewSet,
)

routers = DefaultRouter()
routers.register(r"categories", TicketCategoryViewSet)
routers.register(r"tickets", TicketViewSet)
routers.register(r"comments", TicketCommentViewSet)

urlpatterns = [
    path("", include(routers.urls)),
]