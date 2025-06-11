# messaging_app/chats/views.py

from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .filters import ConversationFilter, MessageFilter
from .permissions import IsParticipantOfConversation # <-- Import the permission
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filterset_class = ConversationFilter
    # Apply our single, powerful permission class
    permission_classes = [IsParticipantOfConversation] 

    def get_queryset(self):
        return self.request.user.conversations.all()

    def get_serializer_context(self):
        return {'request': self.request}

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination 

    def get_queryset(self):
        conversation_pk = self.kwargs['conversation_pk']
        # The permission class will ensure the user has access to this conversation
        return Message.objects.filter(conversation__pk=conversation_pk)

    def perform_create(self, serializer):
        # The permission class already verified access, so this is safe.
        conversation_pk = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_pk)
        serializer.save(sender=self.request.user, conversation=conversation)
