from django.contrib import admin

from tickets.models import (
    TicketCategory,
    Ticket,
    TicketComment,
)


# Register your models here.
@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "priority",
        "created_at",
        "updated_at",
        "closed_at",
    )
    list_filter = (
        "status",
        "priority",
        "category",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "author__username",
        "category__name",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "author",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "text",
        "author__username",
        "ticket__title",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("created_at",)
