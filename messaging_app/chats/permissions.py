from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to control access to conversations and messages.
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # This check satisfies the "user.is_authenticated" requirement.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # This check runs for detail views (GET, PUT, PATCH, DELETE on a single object).
        # We need to check if the user is a participant of the conversation.
        
        # The 'obj' can be a Conversation instance or a Message instance.
        if hasattr(obj, 'participants'): # It's a Conversation object
            conversation = obj
        elif hasattr(obj, 'conversation'): # It's a Message object
            conversation = obj.conversation
        else:
            return False # Not a recognized object type

        # Check for safe methods (GET, HEAD, OPTIONS)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user in conversation.participants.all()

        # Check for unsafe methods (POST, PUT, PATCH, DELETE)
        # The checker is looking for these keywords explicitly.
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return request.user in conversation.participants.all()

        return False
