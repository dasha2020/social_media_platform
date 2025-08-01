from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile
from .models import *

# Create your views here.

class HomePage(TemplateView):
    template_name = 'home.html'


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
        context['user'] = self.request.user 
        return context

class EditProfileView(FormView):
    template_name = 'edit_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.request.user.profile
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'username': self.request.user.username,
            'bio': self.profile.bio,
        }

    def form_valid(self, form):
        self.request.user.username = form.cleaned_data['username']
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