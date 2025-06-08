
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# A ViewSet for viewing and editing Conversation instances.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    # queryset defines the collection of objects that are available for this view.
    # Here, we only show conversations that the currently logged-in user is a part of.
    # self.request.user gets the user making the API request.
    def get_queryset(self):
        user = self.request.user
        return user.conversations.all()

    # serializer_class tells the viewset which serializer to use for the data.
    serializer_class = ConversationSerializer

    # permission_classes ensures that only authenticated users can access this endpoint.
    permission_classes = [permissions.IsAuthenticated]

    # We can override the 'create' method if we need custom logic.
    def perform_create(self, serializer):
        # When creating a new conversation, we automatically add the creator
        # as a participant. The other participants would be sent in the request data.
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


# A ViewSet for viewing and editing Message instances.
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or sent.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # We override the 'create' method to set the sender automatically.
    def perform_create(self, serializer):
        # When a user sends a message, we automatically set the 'sender'
        # to be the currently logged-in user. They don't need to specify it.
        serializer.save(sender=self.request.user)