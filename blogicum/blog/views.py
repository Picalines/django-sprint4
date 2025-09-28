from core.constants import POSTS_BY_PAGE
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView

from .models import Category, Post


def index(request):
    post_list = Post.filter_visible(Post.objects)[:POSTS_BY_PAGE]
    return render(request, "blog/index.html", {"post_list": post_list})


class ProfileDetailView(DetailView):
    template_name = 'blog/profile.html'
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'


def post_detail(request, post_id):
    post = get_object_or_404(Post.filter_visible(Post.objects), id=post_id)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = Post.filter_visible(category.posts)
    return render(
        request,
        "blog/category.html",
        {"post_list": post_list, "category": category},
    )
