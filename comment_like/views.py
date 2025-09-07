from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Comment, Like
from social_media_app.models import Post
from .forms import CommentForm, CommentEditForm
from notification.models import Notification


# Create your views here.

def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)

    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        Notification.objects.filter(from_user=request.user, type="like", like=like).delete()
        like.delete()
        
        liked = False
    else:
        like = Like.objects.create(user=request.user, post=post)
        Notification.objects.create(from_user=request.user, to_user=post.user, type="like", like=like)
        liked = True

    like_count = Like.objects.filter(post=post).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

def add_comment(request, post_id):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = Post.objects.get(id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment.objects.create(user=request.user, post=post, content=content)
            Notification.objects.create(from_user=request.user, to_user=post.user, type="comment", comment=comment)
            



            comments_html = render_to_string('partials/block_comments.html', {'post': post}, request=request)
            return JsonResponse({'status': 'success', 'comments_html': comments_html})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

class DeleteCommentView(View):
    def post(self, request, comment_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            comment = Comment.objects.get(id=comment_id)
            Notification.objects.filter(from_user=request.user, type="like", comment=comment).delete()
            post = comment.post
            comment.delete()
            



            comments_html = render_to_string('partials/block_comments.html', {'post': post}, request=request)
            return JsonResponse({'status': 'success', 'comments_html': comments_html})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
        

class EditCommentView(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        form = CommentEditForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data['content']
            post = comment.post
            comment.save()
            print(post.top_level_comments)

            
            comments_html = render_to_string('partials/block_comments.html', {'post': post}, request=request)
            return JsonResponse({'status': 'success', 'comments_html': comments_html})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    

class ReplyCommentView(View):
    def post(self, request, comment_id):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

        parent_comment = Comment.objects.get(id=comment_id)
        post = parent_comment.post
        content = request.POST.get('content', '').strip()

        if not content:
            return JsonResponse({'status': 'error', 'message': 'Content is required'}, status=400)

        reply = Comment.objects.create(
            user=request.user,
            post=post,
            content=content,
            comment_of_reply=parent_comment
        )
        post.top_level_comments = Comment.objects.filter(
            post=post,
            comment_of_reply__isnull=True
        ).prefetch_related('replies').order_by('-created_at')



        comments_html = render_to_string('partials/block_comments.html', {'post': post}, request=request)
        return JsonResponse({'status': 'success', 'comments_html': comments_html})
