from django.urls import path

from .views import (
    CategoryDetailView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    IndexPage,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    ProfileDetailView,
    ProfileUpdateView,
)

app_name = 'blog'


urlpatterns = [
    path(
        'profile/<slug:username>/', ProfileDetailView.as_view(), name='profile'
    ),
    path('edit_profile', ProfileUpdateView.as_view(), name='edit_profile'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'posts/<int:post_id>/comment/',
        CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment',
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryDetailView.as_view(),
        name='category_posts',
    ),
    path('', IndexPage.as_view(), name='index'),
]
