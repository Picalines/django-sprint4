from core.constants import POSTS_PER_PAGE
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreatePostForm
from .models import Category, Post


class IndexPage(ListView):
    template_name = 'blog/index.html'
    queryset = Post.with_comment_counts(Post.public(Post.objects)).order_by(
        '-pub_date'
    )
    paginate_by = POSTS_PER_PAGE


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

        posts = Post.of_author(Post.objects, author)
        if viewer != author:
            posts = Post.public(posts)
        posts = Post.with_comment_counts(posts).order_by('-pub_date')

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
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = CreatePostForm
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        user = self.request.user
        return reverse('blog:profile', kwargs={'username': user.username})


class CategoryDetailView(DetailView):
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.filter(is_published=True)
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.with_comment_counts(
            Post.public(self.object.posts)
        ).order_by('-pub_date')
        page_number = self.request.GET.get('page')
        paginator = Paginator(posts, POSTS_PER_PAGE)
        context['page_obj'] = paginator.get_page(page_number)
        return context
