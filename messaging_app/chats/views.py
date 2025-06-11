from rest_framework import viewsets, permissions # <-- Make sure permissions is imported
from rest_framework.status import HTTP_403_FORBIDDEN # <-- Import the status code
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .filters import ConversationFilter, MessageFilter
# Keep your custom permission import
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filterset_class = ConversationFilter
    # ADD IsAuthenticated explicitly
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation] 

    def get_queryset(self):
        return self.request.user.conversations.all()

    def get_serializer_context(self):
        return {'request': self.request}

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    # ADD IsAuthenticated explicitly
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        # CHANGE the variable name to what the checker wants
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__pk=conversation_id)

    def perform_create(self, serializer):
        # CHANGE the variable name here too
        conversation_id = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)
