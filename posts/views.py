from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth import authenticate, login
from .forms import PostForm, SignUpForm, CommentForm
from posts.models import Post, PostView, User, Category, Like
from django.http import HttpResponseRedirect

import datetime

from slugify import slugify
import uuid

class PostListView(ListView):
    model = Post
    # paginate_by = 12
    ordering = ['-publish_date']

    def get_queryset(self):
        start_date = datetime.date(2021, 12, 1)
        today_date = datetime.datetime.now()

        from_date = self.request.GET.get('from', start_date)
        to_date = self.request.GET.get('to', today_date)

        if isinstance(from_date, str):
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        if isinstance(to_date, str):
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        category = self.request.GET.get('category', 'ALL')

        query = Post.objects.filter(publish_date__gte=from_date)
        query = query.filter(publish_date__lte=to_date)
        if category != 'ALL':
            query = query.filter(category=category)
        query = query.order_by('-publish_date')
        return query

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        categories = Category.objects.all().values_list('pk', 'name')
        context['categories'] = categories
        # context['elementos'] = 'ELEMENTOS'
        return context

class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect('detail', slug=post.slug)
            
        return redirect('detail', slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()    
        })
        
        return context

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)

        return object

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
        context.update({'view_type': 'create'})
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
        context.update({'view_type': 'create'})
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
        context.update({"view_type": 'Update'})
        return context

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect('detail', slug=slug)