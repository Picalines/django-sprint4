from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import CommentForm, PostForm
from blog.mixins import NoPermissionRedirectMixin, SuccessUrlArgsMixin
from blog.models import Category, Comment, Post, User
from blog.service import get_page_obj
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
        context['page_obj'] = get_page_obj(
            self.request,
            Post.objects.of_author(self.object)
            .visible_for(self.request.user)
            .with_comment_counts()
            .from_old_to_new(),
            POSTS_PER_PAGE,
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessUrlArgsMixin, UpdateView):
    template_name = 'blog/user.html'
    model = User
    fields = ('first_name', 'last_name', 'username', 'email')
    success_url = 'blog:profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url_args(self):
        return [self.object.username]


class PostCreateView(LoginRequiredMixin, SuccessUrlArgsMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    success_url = 'blog:profile'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url_args(self):
        return [self.request.user.username]


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


class PostUpdateView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserPassesTestMixin,
    SuccessUrlArgsMixin,
    UpdateView,
):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    no_permission_url = 'blog:post_detail'
    success_url = 'blog:post_detail'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url_args(self):
        return [self.object.pk]


class PostDeleteView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserPassesTestMixin,
    SuccessUrlArgsMixin,
    DeleteView,
):
    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'
    no_permission_url = 'blog:post_detail'
    success_url = 'blog:profile'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url_args(self):
        return [self.request.user.username]


class CommentCreateView(LoginRequiredMixin, SuccessUrlArgsMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = 'blog:post_detail'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post.objects.filter(pk=self.kwargs['post_id']).visible_for(
                self.request.user
            )
        )
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url_args(self):
        return [self.kwargs['post_id']]


class CommentUpdateView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserPassesTestMixin,
    SuccessUrlArgsMixin,
    UpdateView,
):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'
    form_class = CommentForm
    no_permission_url = 'blog:post_detail'
    no_permission_kwargs = ['post_id']
    success_url = 'blog:post_detail'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url_args(self):
        return [self.object.post.pk]


class CommentDeleteView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserPassesTestMixin,
    SuccessUrlArgsMixin,
    DeleteView,
):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'
    no_permission_url = 'blog:post_detail'
    no_permission_kwargs = ['post_id']
    success_url = 'blog:post_detail'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url_args(self):
        return [self.object.post.pk]


class CategoryDetailView(DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.public()
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = get_page_obj(
            self.request,
            self.object.posts.public().with_comment_counts().from_old_to_new(),
            POSTS_PER_PAGE,
        )
        return context
