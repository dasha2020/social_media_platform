from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm, SearchForm, PostForm, EditPostForm
from comment_like.forms import CommentForm
from comment_like.models import Comment
from notification.models import Notification
from .models import Profile
from .models import *
from django.core.paginator import Paginator
import os
from django.conf import settings
from django.http import JsonResponse

# Create your views here.

class HomePage(FormView):
    template_name = 'home.html'
    form_class = SearchForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context

    def get(self, request, *args, **kwargs):
        username = self.request.GET.get('username')
        if username:
            return redirect('search_users', username=username)
        
        if request.user.is_authenticated:
            user = request.user
            followings = request.user.following.all()
            list_of_following = []
            recent_posts = []
            for following in followings:
                list_of_following.append(following.following)
            
            for following in list_of_following:
                latest_post = Post.objects.filter(user=following).order_by("-created_at")[:4]
                for late_post in latest_post:
                    recent_posts.append(late_post)
            print(recent_posts)
            posts = Post.objects.filter(user=user).order_by("-created_at")
            paginator = Paginator(recent_posts, 3)  
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            posts_count = posts.count()
            form_c = CommentForm
            for post in page_obj:
                post.liked = post.likes.filter(user=request.user).exists()
            context = self.get_context_data(form=self.get_form(), posts=page_obj, form_comments=form_c)
        else:
        
            context = self.get_context_data(form=self.get_form())

        return render(request, "home.html", context)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if username:
            return redirect('find_user', username=username)
        return super().form_valid(form)

def beginning(request):
    
    image_dir = os.path.join(settings.STATICFILES_DIRS[0], 'gallery')
    
    
    images = sorted(os.listdir(image_dir))
    image_urls = [f'/static/gallery/{img}' for img in images if img.lower().endswith(('.jpg', '.png', '.jpeg', '.gif'))]

    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(image_urls, 1)  
    page_obj = paginator.get_page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'images': page_obj.object_list,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        })

    return render(request, 'gallery.html', {'images': page_obj})
    

class SearchUsersView(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    def get(self, request, username):
        users = User.objects.filter(username__icontains=username)
        followings = request.user.following.all()
        list_of_following = []
        for following in followings:
            list_of_following.append(following.following)
        followed_users = [] 
        other_users = []
        for user in users:
            if user in list_of_following:
                followed_users.append(user)
            else:
                other_users.append(user)
        context = self.get_context_data(users=other_users, followings=followed_users)
        return render(request, 'search_users.html', context)

class FindUserView(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        followers = user.followers.count()
        following = user.following.count()
        followed = False
        posts = Post.objects.filter(user=user).order_by("-created_at")
        posts_count = posts.count()
        for post in posts:
            post.liked = post.likes.filter(user=request.user).exists()
        form_c = CommentForm
        if user.followers.filter(follower=request.user).exists():
            followed = True
        context = self.get_context_data(user=user, followers=followers, followed=followed, following=following, posts=posts, posts_count=posts_count, form_comments=form_c)
        return render(request, 'find_user.html', context)
    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        if "unfollow" in request.POST:
            follower = Follower.objects.filter(follower=request.user, following=user)
            Notification.objects.filter(from_user=request.user, to_user=user, type="follower").delete()
            follower.delete()
        else:
            follower = Follower.objects.create(
                follower=request.user,
                following=user
            )
            Notification.objects.create(from_user=request.user, to_user=user, type="follower")
        followers = user.followers.count()
        following = user.following.count()
        followed = False
        if user.followers.filter(follower=request.user).exists():
            followed = True
        context = self.get_context_data(user=user, followers=followers, followed=followed, following=following)
        return render(request, 'find_user.html', context)

class FollowersView(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    def get(self, request):
        user = request.user
        followers = user.followers.all()
        list_of_followers = []
        for follower in followers:
            list_of_followers.append(follower.follower)

        context = self.get_context_data(user=user, followers=list_of_followers)
        return render(request, 'followers_list.html', context)

class FollowingsView(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    def get(self, request):
        user = request.user
        followings = request.user.following.all()
        list_of_following = []
        for following in followings:
            list_of_following.append(following.following)

        context = self.get_context_data(user=user, followings=list_of_following)
        return render(request, 'followings.html', context)

class AddPostView(FormView):
    template_name = 'add_post.html'
    form_class = PostForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        content = form.cleaned_data['content']
        photo = form.cleaned_data.get('photo')

        post = Post.objects.create(user=self.request.user, content=content, photo=photo)
        return super().form_valid(form)

class EditPostView(FormView):
    template_name = 'edit_post.html'
    form_class = EditPostForm
    success_url = reverse_lazy('profile')

    def dispatch(self, request, post_id, *args, **kwargs):
        self.post_object = Post.objects.get(id=post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'content': self.post_object.content,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post_object
        return context

    def form_valid(self, form):
        self.post_object.content = form.cleaned_data['content']
        photo = form.cleaned_data.get('photo')
        if photo:
            self.post_object.photo = photo
        self.post_object.save()
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)

class ProfileView(TemplateView):
    template_name = 'profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get(self, request):
        user = request.user
        followers = user.followers.count()
        following = user.following.count()
        posts = Post.objects.filter(user=user).order_by("-created_at")
        posts_count = posts.count()
        for post in posts:
            post.liked = post.likes.filter(user=request.user).exists()
            



        #comments_html = render_to_string('partials/block_comments.html', {'comments': top_level_comments, 'post': post}, request=request)
        form_c = CommentForm
        form_search = SearchForm
        notifications = Notification.objects.filter(to_user=request.user).count()
        
        context = self.get_context_data(user=user, followers=followers, following=following, posts=posts, posts_count=posts_count, form_comments=form_c, notifications=notifications, form_search=form_search)
        return render(request, 'profile.html', context)
    def post(self, request):
        if 'delete_id' in request.POST:
            post_id = request.POST.get('delete_id')
            post = Post.objects.get(id=post_id, user=request.user)
            post.delete()
        return redirect('profile')

class EditProfileView(FormView):
    template_name = 'edit_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.request.user.profile
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'username': self.profile.user.username,
            'bio': self.profile.bio,
        }

    def form_valid(self, form):
        self.profile.user.username = form.cleaned_data['username']
        self.profile.bio = form.cleaned_data['bio']
        avatar = form.cleaned_data.get('avatar')
        if avatar:
            self.profile.avatar = avatar
        self.profile.save()
        self.profile.user.save()
        return super().form_valid(form)

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')