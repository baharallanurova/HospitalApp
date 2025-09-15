from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'date_created', 'message_preview')
    list_filter = ('date_created', 'user_from', 'user_to')
    search_fields = ('message', 'user_from__username', 'user_to__username')
    date_hierarchy = 'date_created'

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    message_preview.short_description = 'Message Preview'

