from core.constants import POSTS_BY_PAGE
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, TemplateView

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
