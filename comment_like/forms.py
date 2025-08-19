from django import forms
from django.contrib.auth.models import User

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Write your comment...',
        }))


class CommentEditForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput())