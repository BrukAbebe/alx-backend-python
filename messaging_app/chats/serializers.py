# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

# A serializer for our custom User model
# It will show the user's ID and username.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# A serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    # We want to show the sender's username, not just their ID.
    # 'read_only=True' means we can see this field, but we can't set it directly when creating a message.
    # 'source' tells DRF to get the value from 'sender.username'.
    sender = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        # These are the fields that will be converted to/from JSON.
        # We don't need to specify 'sender' here as a field because we defined it above.
        # But we do need 'sender' when creating a message, so we make it write-only.
        fields = ['id', 'sender', 'text', 'timestamp', 'conversation']
        extra_kwargs = {
            'conversation': {'write_only': True} # Don't show the whole conversation object on every message
        }

# A serializer for the Conversation model
class ConversationSerializer(serializers.ModelSerializer):
    # This is a nested serializer. When we view a conversation, we want to see
    # the list of participants and the list of messages inside it.
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True) # 'many=True' as there can be multiple messages

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']