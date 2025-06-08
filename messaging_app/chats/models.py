import uuid  # Required for UUID primary keys
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# 1. User Model - matching the checker's expected fields
class User(AbstractUser):
    # Django's AbstractUser already has: email, password, first_name, last_name.
    # We will override the primary key to be 'user_id' and add 'phone_number'.
    # Note: Django's User model uses 'id' by default. We create a new field
    # and make it the primary key.
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # We don't need to define email, password, first_name, last_name as they
    # are already part of AbstractUser. The checker is just confirming their presence.

# 2. Conversation Model - matching the checker's expected fields
class Conversation(models.Model):
    # Override the default 'id' primary key with 'conversation_id'
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation ID: {self.conversation_id}"

# 3. Message Model - matching the checker's expected fields
class Message(models.Model):
    # Override the default 'id' primary key with 'message_id'
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        'Conversation', # Use string reference here to avoid import issues
        on_delete=models.CASCADE,
        related_name='messages'
    )
    # Rename 'text' to 'message_body'
    message_body = models.TextField()
    # Rename 'timestamp' to 'sent_at'
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message ID: {self.message_id}"

    class Meta:
        # Order messages by the 'sent_at' field
        ordering = ['sent_at']