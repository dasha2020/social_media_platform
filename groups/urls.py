from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('create_group/', views.create_group, name='create_group'),
    path('show_groups/', GroupsListView.as_view(), name='show_groups'),
    path('group/<int:group_id>/', GroupsMessagesView.as_view(), name='group_chat'),
    path('edit/<int:group_id>/', views.edit_message, name='edit_message'),
    path('delete/<int:group_id>/', views.delete_message, name='delete_message'),
    path('<int:group_id>/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
]
