from django.db import models
from django.db.models import fields
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView,UpdateView, DetailView
from .forms import PostForm
from posts.models import Post

from slugify import slugify
import uuid


class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

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
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'view_type': 'Update' 
            })
        return context
    