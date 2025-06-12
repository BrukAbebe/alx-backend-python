from django.urls import path
from . import views

urlpatterns = [
    path('delete-account/', views.delete_user, name='delete_user'),
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
    path('inbox/', views.unread_messages, name='inbox'),
]
