from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from tickets.models import (
    TicketStatus,
    TicketCategory,
    Ticket,
    TicketComment,
)


class TicketCategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TicketCategory
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "created_at",
            "updated_at",
        )


class TicketSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    closed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "author",
            "author_username",
            "category",
            "category_name",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "closed_at",
        )

    def validate(self, attrs):
        request = self.context.get("request")
        ticket_instance = self.instance

        if request is None:
            return attrs

        is_staff_or_superuser = request.user.is_staff or request.user.is_superuser

        if "status" in attrs and not is_staff_or_superuser:
            raise ValidationError("Только администратор может менять статус тикетов")

        if ticket_instance is not None:
            if ticket_instance.status == TicketStatus.CLOSED and not is_staff_or_superuser:
                raise ValidationError("Только администратор может редактировать закрытые тикеты")

        if "status" in attrs and is_staff_or_superuser:
            if attrs["status"] == TicketStatus.CLOSED:
                attrs["closed_at"] = timezone.now()
            else:
                attrs["closed_at"] = None

        return attrs


class TicketCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    ticket_title = serializers.CharField(
        source="ticket.title",
        read_only=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TicketComment
        fields = (
            "id",
            "ticket",
            "ticket_title",
            "author",
            "author_username",
            "text",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        request = self.context.get("request")
        comment_instance = self.instance

        if request is None:
            return attrs

        is_staff_or_superuser = request.user.is_staff or request.user.is_superuser

        ticket = attrs.get("ticket")

        if ticket is None and comment_instance is not None:
            ticket = comment_instance.ticket

        if ticket is None:
            return attrs

        if request.user.id != ticket.author_id and not is_staff_or_superuser:
            raise ValidationError("Только администратор может комментировать тикеты других пользователей")

        if ticket.status == TicketStatus.CLOSED and not is_staff_or_superuser:
            raise ValidationError("Только администратор может комментировать закрытые тикеты")

        return attrs
