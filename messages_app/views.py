from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .models import Chat, ChatMessage
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
class MessageView(TemplateView):
    template_name = 'messages.html'
    def get_context_data(self, **kwargs):
        user = self.request.user
        followers = user.followers.all()
        followings = user.following.all()

        
        connections = []
        print("bla")
        for follower in followers:
            connections.append(follower.follower)
        print(connections)
        chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
        context = super().get_context_data(**kwargs)
        context["connections"] = connections
        context["chats"] = chats
        unread_messages_count = 0
        if self.request.user.is_authenticated:
            unread_messages_count = ChatMessage.objects.filter(
            Q(chat__in=chats) & Q(is_read=False) & ~Q(user=user)
        ).count()
        context["unread_messages_count"] = unread_messages_count
        return context

@login_required
def unread_messages_count_view(request):
    chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    count = ChatMessage.objects.filter(
            Q(chat__in=chats) & Q(is_read=False) & ~Q(user=request.user)
        ).count()
    print(count)
    print(chats)
    return JsonResponse({'unread_messages_count': count})

class MessageListView(TemplateView):
    template_name = 'messages_list.html'
    def get_context_data(self, **kwargs):
        user = self.request.user
        followers = user.followers.all()
        followings = user.following.all()

        
        connections = []
        print("bla")
        for follower in followers:
            connections.append(follower.follower)
        print(connections)
        context = super().get_context_data(**kwargs)
        context["connections"] = connections
        chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
        
        context["chats"] = chats
        return context

def chat_room(request, username):
    other_user = User.objects.get(username=username)
    user = request.user

    if user.id < other_user.id:
        chat, created = Chat.objects.get_or_create(user1=user, user2=other_user)
    else:
        chat, created = Chat.objects.get_or_create(user1=other_user, user2=user)


    print(chat)
    #chat = Chat.objects.filter(chat=chat.id)
    messages = ChatMessage.objects.filter(chat=chat.id).order_by('created_at')
    if user != other_user:
        messages1 = chat.messages.filter(user=other_user,is_read=False)
        messages1.update(is_read=True)
    print(messages)
    return render(request, 'chat_room.html', {
        'other_user': other_user,
        'messages': messages,
    })


def edit_message(request, message_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
    message = ChatMessage.objects.get(id=message_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't edit this message.")
    
    new_text = request.POST.get('text', '').strip()
    if new_text:
        message.text = new_text
        message.save()
        return JsonResponse({'status': 'success', 'text': message.text})
    
    return JsonResponse({'status': 'error', 'message': 'Empty text'}, status=400)


def delete_message(request, message_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
    message = ChatMessage.objects.get(id=message_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't delete this message.")
    
    message.delete()
    return JsonResponse({'status': 'success'})