from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('notification/', NotificationView.as_view(), name='notification_show'),
    path('count/', views.notification_count, name='notification_count'),
]