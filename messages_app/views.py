from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .models import Chat, ChatMessage
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

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
        context = super().get_context_data(**kwargs)
        context["connections"] = connections
        return context

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
        return context

def chat_room(request, username):
    other_user = User.objects.get(username=username)
    user = request.user

    if user.id < other_user.id:
        chat, created = Chat.objects.get_or_create(user1=user, user2=other_user)
    else:
        chat, created = Chat.objects.get_or_create(user1=other_user, user2=user)


    print(chat)
    
    messages = ChatMessage.objects.filter(chat=chat.id).order_by('created_at')
    print(messages)
    return render(request, 'chat_room.html', {
        'other_user': other_user,
        'messages': messages,
    })

@require_POST
def edit_message(request, message_id):
    message = ChatMessage.objects.get(id=message_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't edit this message.")
    
    new_text = request.POST.get('text', '').strip()
    if new_text:
        message.text = new_text
        message.save()
        return JsonResponse({'status': 'success', 'text': message.text})
    
    return JsonResponse({'status': 'error', 'message': 'Empty text'}, status=400)

@require_POST
def delete_message(request, message_id):
    message = ChatMessage.objects.get(id=message_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't delete this message.")
    
    message.delete()
    return JsonResponse({'status': 'success'})