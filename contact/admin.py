from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "liked_site", "created_at", "is_read"]
    list_filter = ["is_read", "liked_site"]
    list_editable = ["is_read"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["name", "email", "liked_site", "message", "created_at"]
