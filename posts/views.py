from django.db import models
from django.db.models import fields
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView,UpdateView, DetailView
from django.contrib.auth import authenticate, login
from .forms import PostForm, SignUpForm
from posts.models import Post, User
from django.http import HttpResponseRedirect

from slugify import slugify
import uuid


class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

class UserCreateView(CreateView):
    form_class = SignUpForm
    model = User
    template_name_suffix = '_signup'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'view_type': 'create' })
        return context
    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name_suffix = '_create'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'view_type': 'create' })
        return context
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title) + '_' + str(uuid.uuid4())[:8]
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name_suffix = '_update'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'view_type': 'Update' 
            })
        return context
    