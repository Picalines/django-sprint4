from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import CommentForm, PostForm
from blog.mixins import (
    NoPermissionRedirectMixin,
    SubListMixin,
    SuccessUrlArgsMixin,
    UserIsAuthorMixin,
)
from blog.models import Category, Comment, Post, User
from core.constants import POSTS_PER_PAGE


class IndexPage(ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = Post.objects.public().with_comment_counts().from_old_to_new()


class ProfileDetailView(SubListMixin, DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'
    paginate_sublist_by = POSTS_PER_PAGE

    def get_sublist_queryset(self):
        return (
            Post.objects.of_author(self.object)
            .visible_for(self.request.user)
            .with_comment_counts()
            .from_old_to_new()
        )


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
    UserIsAuthorMixin,
    SuccessUrlArgsMixin,
    UpdateView,
):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    no_permission_url = 'blog:post_detail'
    success_url = 'blog:post_detail'

    def get_success_url_args(self):
        return [self.object.pk]


class PostDeleteView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserIsAuthorMixin,
    SuccessUrlArgsMixin,
    DeleteView,
):
    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'
    no_permission_url = 'blog:post_detail'
    success_url = 'blog:profile'

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
    UserIsAuthorMixin,
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

    def get_success_url_args(self):
        return [self.object.post.pk]


class CommentDeleteView(
    LoginRequiredMixin,
    NoPermissionRedirectMixin,
    UserIsAuthorMixin,
    SuccessUrlArgsMixin,
    DeleteView,
):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'
    no_permission_url = 'blog:post_detail'
    no_permission_kwargs = ['post_id']
    success_url = 'blog:post_detail'

    def get_success_url_args(self):
        return [self.object.post.pk]


class CategoryDetailView(SubListMixin, DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.public()
    context_object_name = 'category'
    paginate_sublist_by = POSTS_PER_PAGE

    def get_sublist_queryset(self):
        return (
            self.object.posts.public().with_comment_counts().from_old_to_new()
        )
