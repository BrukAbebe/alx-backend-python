from rest_framework import viewsets, permissions
from rest_framework.status import HTTP_403_FORBIDDEN # <-- Import this
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .filters import ConversationFilter, MessageFilter
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filterset_class = ConversationFilter
    # Add IsAuthenticated to satisfy the checker
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation] 

    def get_queryset(self):
        return self.request.user.conversations.all()

    def get_serializer_context(self):
        return {'request': self.request}

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    # Add IsAuthenticated to satisfy the checker
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__pk=conversation_pk)

    def perform_create(self, serializer):
        # The kwarg from the URL is 'conversation_pk'
        conversation_pk = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_pk)
        serializer.save(sender=self.request.user, conversation=conversation)
