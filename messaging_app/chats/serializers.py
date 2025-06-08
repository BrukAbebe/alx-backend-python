from rest_framework import serializers
from .models import User, Conversation, Message

# We need to import ValidationError
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Use the new primary key 'user_id' and other relevant fields
        fields = ['user_id', 'username', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    # Display the sender's username for readability
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        # Update fields to match the new model definitions
        fields = ['message_id', 'sender_username', 'message_body', 'sent_at', 'conversation']
        # Hide the conversation field from the read representation
        extra_kwargs = {
            'conversation': {'write_only': True}
        }

class ConversationSerializer(serializers.ModelSerializer):
    # This shows the full details of the participants, which is good.
    participants = UserSerializer(many=True, read_only=True)
    # This shows all messages within the conversation.
    messages = MessageSerializer(many=True, read_only=True)
    
    # We will add a new field that is not on the model directly.
    # This will satisfy the "SerializerMethodField" requirement.
    conversation_name = serializers.SerializerMethodField()
    
    # We will add a write-only field to accept participant user_ids when creating a conversation
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = Conversation
        # Update fields to match the new model definitions and add our new fields
        fields = ['conversation_id', 'conversation_name', 'participants', 'participant_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at', 'participants', 'messages']

    # This method is linked to the "conversation_name" SerializerMethodField.
    # The name must be get_<field_name>.
    def get_conversation_name(self, obj):
        """
        Generates a readable name for the conversation, like "Chat with user1, user2".
        """
        # Exclude the current user from the display name for a cleaner look in a 2-person chat
        current_user = self.context['request'].user
        other_participants = [p.username for p in obj.participants.all() if p != current_user]
        if not other_participants:
             return f"Chat with {current_user.username}"
        return f"Chat with {', '.join(other_participants)}"

    # This is the custom validation method.
    # It will satisfy the "ValidationError" requirement.
    def validate_participant_ids(self, value):
        """
        Check that the list of participant IDs is not empty and users exist.
        """
        if not value:
            raise ValidationError("You must provide at least one participant_id.")
        
        # Check if all provided UUIDs correspond to actual users
        for user_id in value:
            if not User.objects.filter(user_id=user_id).exists():
                raise ValidationError(f"User with id {user_id} does not exist.")
        return value

    def create(self, validated_data):
        """
        Custom create method to handle creating a conversation and adding participants.
        """
        participant_ids = validated_data.pop('participant_ids')
        current_user = self.context['request'].user
        
        # Create the conversation instance
        conversation = Conversation.objects.create(**validated_data)
        
        # Add the current user to the participants
        conversation.participants.add(current_user)
        
        # Add the other participants from the provided list
        for user_id in participant_ids:
            user_to_add = User.objects.get(user_id=user_id)
            conversation.participants.add(user_to_add)
            
        return conversation