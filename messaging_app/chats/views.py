
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


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or sent within a specific conversation.
    """
    serializer_class = MessageSerializer
    # permission_classes are now handled globally by the settings.py file

    def get_queryset(self):
        """
        This view should return a list of all the messages for
        the conversation as determined by the conversation_pk portion of the URL.
        """
        # Get the conversation_pk from the URL
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__pk=conversation_pk)

    def perform_create(self, serializer):
        """
        Set the sender and the conversation automatically based on the context.
        """
        conversation_pk = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_pk)
        # Set the sender to the logged-in user
        serializer.save(sender=self.request.user, conversation=conversation)
