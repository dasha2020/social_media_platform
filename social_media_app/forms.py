from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=85, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'john'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))



class LoginForm(forms.Form):
    username = forms.CharField(max_length=85, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'john'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Type here...'}))

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=85, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    avatar = forms.ImageField(required=False)


class SearchForm(forms.Form):
    username = forms.CharField(max_length=85, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'john'}))

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Write your caption...',
            'rows': 4,
            'cols': 85
        }))
    photo = forms.ImageField(required=False)

class EditPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Write your caption...',
            'rows': 4,
            'cols': 85
        }))
    photo = forms.ImageField(required=False)
