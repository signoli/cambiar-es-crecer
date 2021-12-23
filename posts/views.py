from django.db import models
from django.db.models import fields
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.contrib.auth import authenticate, login
from .forms import PostForm, SignUpForm
from posts.models import Post, User, Category
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

        if from_date is 'string':
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
        if to_date is 'string':
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
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
