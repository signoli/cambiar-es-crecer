from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView,UpdateView, DetailView

from posts.models import Post


class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post

class PostCreateView(CreateView):
    model = Post

class PostUpdateView(UpdateView):
    model = Post