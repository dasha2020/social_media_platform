from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from .models import Group, GroupMessage
from django.contrib.auth.models import User
import json
from django.views.generic import TemplateView, View

# Create your views here.

def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        member_ids = data['members']
        group = Group.objects.create(name=name, admin=request.user)
        group.users.set(User.objects.filter(id__in=member_ids + [request.user.id]))
        return JsonResponse({'status': 'success', 'group_id': group.id})

class GroupsListView(TemplateView):
    template_name = 'groups_messages.html'
    def get_context_data(self, **kwargs):
        user = self.request.user
        followers = user.followers.all()
        followings = user.following.all()

        
        connections = []
        print("bla")
        for follower in followers:
            connections.append(follower.follower)
        for following in followings:
            if following.following not in connections:
                connections.append(following.following)
        print(connections)
        groups = Group.objects.filter(users=self.request.user)
        context = super().get_context_data(**kwargs)
        context["users"] = connections
        context["groups"] = groups
        return context

class GroupsMessagesView(TemplateView):
    template_name = 'group_chat_show.html'
    def get_context_data(self, **kwargs):
        user = self.request.user
        group_id = self.kwargs.get('group_id')
        group = Group.objects.get(id=group_id)
        context = super().get_context_data(**kwargs)
        messages = GroupMessage.objects.filter(group=group).order_by('created_at')

        context['group'] = group
        context['messages'] = messages
        context['user'] = self.request.user
        return context

def edit_message(request, group_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
    message = GroupMessage.objects.get(id=group_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't edit this message.")
    
    new_text = request.POST.get('text', '').strip()
    if new_text:
        message.text = new_text
        message.save()
        return JsonResponse({'status': 'success', 'text': message.text})
    
    return JsonResponse({'status': 'error', 'message': 'Empty text'}, status=400)


def delete_message(request, group_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
    message = GroupMessage.objects.get(id=group_id)
    
    if request.user != message.user:
        return HttpResponseForbidden("You can't delete this message.")
    
    message.delete()
    return JsonResponse({'status': 'success'})

def delete_user(request, group_id, user_id):
    try:
        group = Group.objects.get(id=group_id)

        if group.admin != request.user:
            return HttpResponseForbidden("You are not admin")

        user_delete = User.objects.get(id=user_id)

        if user_delete == group.admin:
            return JsonResponse({'error': 'Admin can''t delete themselves'}, status=400)

        group.users.remove(user_delete)

        return JsonResponse({'status': 'success'})
    
    except Group.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=404)
