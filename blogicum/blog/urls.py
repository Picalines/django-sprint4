from django.urls import path

from .views import (
    CategoryDetailView,
    IndexPage,
    PostDetailView,
    ProfileDetailView,
)

app_name = 'blog'


urlpatterns = [
    path(
        'profile/<slug:username>/', ProfileDetailView.as_view(), name='profile'
    ),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'category/<slug:category_slug>/',
        CategoryDetailView.as_view(),
        name='category_posts',
    ),
    path('', IndexPage.as_view(), name='index'),
]
