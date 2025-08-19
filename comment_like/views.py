from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Comment, Like
from social_media_app.models import Post
from .forms import CommentForm, CommentEditForm


# Create your views here.

def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)

    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True

    like_count = Like.objects.filter(post=post).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('profile')

class DeleteCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect('profile')

class EditCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        form = CommentEditForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data['content']
            comment.save()
        return redirect('profile')
