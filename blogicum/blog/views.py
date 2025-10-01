from typing import cast

from core.constants import POSTS_PER_PAGE
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


class IndexPage(ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = (
        Post.objects.public()
        .with_comment_counts()
        .from_old_to_new()
        .select_related('location', 'author')
    )


class ProfileDetailView(DetailView):
    template_name = 'blog/profile.html'
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        viewer = self.request.user
        author = self.object

        posts = (
            Post.objects.of_author(author)
            .visible_for(viewer)
            .with_comment_counts()
            .from_old_to_new()
            .select_related('category', 'location')
        )

        page_number = self.request.GET.get('page')
        paginator = Paginator(posts, POSTS_PER_PAGE)
        context['page_obj'] = paginator.get_page(page_number)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    model = get_user_model()
    fields = ('first_name', 'last_name', 'username', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.object.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_at = now()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse('blog:profile', kwargs={'username': user.username})


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['post_id']).visible_for(
            self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.of_post(
            self.object
        ).select_related('author')
        return context


class PostUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})

    def handle_no_permission(self):
        return redirect(
            reverse(
                'blog:post_detail', kwargs={'post_id': self.get_object().pk}
            )
        )


class PostDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        user = self.request.user
        return reverse('blog:profile', kwargs={'username': user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    _post = cast(Post, None)

    def dispatch(self, request, *args, **kwargs):
        self._post = get_object_or_404(
            Post.objects.filter(pk=kwargs['post_id']).visible_for(request.user)
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self._post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self._post.pk})


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'
    form_class = CommentForm

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.post.pk}
        )


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.post.pk}
        )


class CategoryDetailView(DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.public()
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = (
            self.object.posts.public()
            .with_comment_counts()
            .from_old_to_new()
            .select_related('author', 'location')
        )
        page_number = self.request.GET.get('page')
        paginator = Paginator(posts, POSTS_PER_PAGE)
        context['page_obj'] = paginator.get_page(page_number)
        return context
