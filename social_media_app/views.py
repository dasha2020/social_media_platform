from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm, SearchForm, PostForm, EditPostForm
from .models import Profile
from .models import *

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
                latest_post = Post.objects.filter(user=following).order_by("-created_at").first()
                if latest_post:
                    recent_posts.append(latest_post)
            print(recent_posts)
            context = self.get_context_data(form=self.get_form(), posts=recent_posts)
        else:
        
            context = self.get_context_data(form=self.get_form())

        return render(request, "home.html", context)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if username:
            return redirect('find_user', username=username)
        return super().form_valid(form)

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
        if user.followers.filter(follower=request.user).exists():
            followed = True
        context = self.get_context_data(user=user, followers=followers, followed=followed, following=following)
        return render(request, 'find_user.html', context)
    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        if "unfollow" in request.POST:
            follower = Follower.objects.filter(follower=request.user, following=user)
            follower.delete()
        else:
            follower = Follower.objects.create(
                follower=request.user,
                following=user
            )
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
        context = self.get_context_data(user=user, followers=followers, following=following, posts=posts)
        return render(request, 'profile.html', context)
    def post(self, request):
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
        self.request.user.save()
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