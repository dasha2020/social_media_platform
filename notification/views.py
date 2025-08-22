from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def notification_count(request):
    count = request.user.notifications.count()
    return JsonResponse({'count': count})

class NotificationView(TemplateView):
    template_name = 'notification.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(to_user=user)

        context = self.get_context_data(user=user, notifications=notifications)
        return render(request, 'notification.html', context)

