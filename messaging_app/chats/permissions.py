from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to see it.
    """
    def has_object_permission(self, request, view, obj):
        # The `obj` here is a Conversation instance.
        # We check if the requesting user is in the conversation's participants.
        return request.user in obj.participants.all()
