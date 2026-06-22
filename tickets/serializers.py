from rest_framework import serializers

from tickets.models import (
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

