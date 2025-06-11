from django_filters.rest_framework import FilterSet, CharFilter, DateTimeFilter
from .models import Conversation, Message

class ConversationFilter(FilterSet):
    """
    Filter for conversations based on participant username.
    """
    username = CharFilter(field_name='participants__username', lookup_expr='icontains')

    class Meta:
        model = Conversation
        fields = ['username']

class MessageFilter(FilterSet):
    """
    Filter for messages based on a date range.
    """
    start_date = DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['start_date', 'end_date']
