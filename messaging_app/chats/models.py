# messaging_app/chats/models.py

from django.db import models
from django.conf import settings # <-- IMPORT THIS
from django.contrib.auth.models import AbstractUser

# This model definition is correct and does not need to change.
class User(AbstractUser):
    pass

class Conversation(models.Model):
    # CHANGED HERE: We now refer to the User model via the settings string.
    # This is the recommended Django best practice.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # We need to fetch the User model class to work with it here.
        user_model = settings.AUTH_USER_MODEL.split('.')[-1]
        # This part is a bit more complex to get participant names but is robust.
        # A simpler way is to just return the conversation ID if this causes issues.
        return f"Conversation ID: {self.id}"

class Message(models.Model):
    # CHANGED HERE: Same change for the ForeignKey.
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    # This relationship is to a model within the same app, so no change is needed.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Since 'sender' is a relation to AUTH_USER_MODEL, accessing sender.username works fine.
        return f"From {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp']