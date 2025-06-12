from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.views.decorators.cache import cache_page
from .models import Message
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Adjust redirect as needed
    return render(request, 'messaging/delete_account.html')

@login_required
@cache_page(60)
def conversation_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).only('id', 'content', 'timestamp', 'sender__username', 'receiver__username', 'parent_message_id')
    context = {
        'messages': messages,
        'other_user': other_user
    }
    return render(request, 'messaging/conversation.html', context)

@login_required
def unread_messages(request):
    unread_messages = Message.unread.filter(receiver=request.user).only(
        'id', 'content', 'timestamp', 'sender__username'
    )
    context = {'unread_messages': unread_messages}
    return render(request, 'messaging/inbox.html', context)
