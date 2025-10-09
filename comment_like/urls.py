from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('comments/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('reply_comment/<int:comment_id>/', ReplyCommentView.as_view(), name='reply_comment'),
    path('comment_count/<int:post_id>/', comment_count_view, name='comment_count'),
    path('like_count/<int:post_id>/', views.like_count_view, name='like_count'),
]