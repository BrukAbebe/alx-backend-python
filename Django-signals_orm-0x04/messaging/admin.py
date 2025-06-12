from django.contrib import admin
from .models import Message, Notification, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'timestamp', 'edited', 'read']
    list_filter = ['timestamp', 'edited', 'read']
    search_fields = ['content', 'sender__username', 'receiver__username']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at', 'read']
    list_filter = ['created_at', 'read']
    search_fields = ['user__username']

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['message', 'old_content', 'edited_at']
    list_filter = ['edited_at']
    search_fields = ['old_content']
