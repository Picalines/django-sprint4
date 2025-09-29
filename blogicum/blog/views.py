from core.constants import POSTS_BY_PAGE
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .forms import CreatePostForm
from .models import Category, Post


class IndexPage(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'post_list': Post.filter_visible(Post.objects)[:POSTS_BY_PAGE],
        }


class ProfileDetailView(DetailView):
    template_name = 'blog/profile.html'
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    model = get_user_model()
    fields = ('first_name', 'last_name', 'username', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        user = self.get_object()
        return reverse('blog:profile', kwargs={'username': user.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_at = now()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse('blog:profile', kwargs={'username': user.username})


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    queryset = Post.filter_visible(Post.objects)
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'


class CategoryDetailView(DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.filter(is_published=True)
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'post_list': Post.filter_visible(self.object.posts),
        }
