from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm

from .models import Post, User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'thumbnail']
        labels = {
            'category': 'Categoría',
            'title': 'Título',
            'content': 'Contenido',
            'thumbnail': 'Imagen',
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']