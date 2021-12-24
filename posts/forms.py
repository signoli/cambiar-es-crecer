from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

from .models import Post, User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','category', 'thumbnail']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'category': 'Categoría',
            'thumbnail': 'Imagen',
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows': 3,
    }))
    class Meta:
        model = Comment
        fields = ('content',)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
