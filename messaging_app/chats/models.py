from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. User Model
# We extend Django's built-in AbstractUser. This gives us fields like
# username, password, email, etc., for free. We can add more fields here
# if we needed to (e.g., a profile picture). For now, we'll just use the base.
class User(AbstractUser):
    pass # pass means we are not adding any extra fields for now

# 2. Conversation Model
# This model represents a chat session between two or more users.
class Conversation(models.Model):
    # 'participants' is a ManyToManyField. This means a User can be in many
    # Conversations, and a Conversation can have many Users.
    # 'related_name' lets us easily access the conversations from a user object
    # For example: my_user.conversations.all()
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}"

# 3. Message Model
# This model represents a single message within a conversation.
class Message(models.Model):
    # 'sender' is a ForeignKey, representing a one-to-many relationship.
    # One User can send many Messages.
    # 'on_delete=models.CASCADE' means if a User is deleted, all their messages
    # will be deleted too.
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')

    # 'conversation' is also a ForeignKey. One Conversation can have many Messages.
    # If a Conversation is deleted, all its messages are deleted.
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    # The actual text content of the message.
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp'] # Ensure messages are ordered by when they were sent