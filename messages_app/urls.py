from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('messages_show/', MessageView.as_view(), name='messages_show'),
    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('unread_messages_count/', views.unread_messages_count_view, name='unread_messages_count'),
]