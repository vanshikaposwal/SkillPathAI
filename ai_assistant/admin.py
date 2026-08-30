from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'message', 'timestamp']
    list_filter = ['role', 'timestamp']
    search_fields = ['user__username', 'message']
