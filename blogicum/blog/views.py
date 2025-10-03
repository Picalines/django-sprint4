from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post, User
from core.constants import POSTS_PER_PAGE


class IndexPage(ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = Post.objects.public().with_comment_counts().from_old_to_new()


class ProfileDetailView(DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = (
            Post.objects.of_author(self.object)
            .visible_for(self.request.user)
            .with_comment_counts()
            .from_old_to_new()
        )
        context['page_obj'] = Paginator(posts, POSTS_PER_PAGE).get_page(
            self.request.GET.get('page')
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    model = User
    fields = ('first_name', 'last_name', 'username', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.username])


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['post_id']).visible_for(
            self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.of_post(self.object)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])

    def handle_no_permission(self):
        return redirect(
            reverse('blog:post_detail', args=[self.get_object().pk])
        )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post.objects.filter(pk=self.kwargs['post_id']).visible_for(
                self.request.user
            )
        )
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'
    form_class = CommentForm

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.pk])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.pk])


class CategoryDetailView(DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.public()
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = (
            self.object.posts.public().with_comment_counts().from_old_to_new()
        )
        context['page_obj'] = Paginator(posts, POSTS_PER_PAGE).get_page(
            self.request.GET.get('page')
        )
        return context
