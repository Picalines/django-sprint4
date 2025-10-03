from django.db import models

from blog.querysets import CategoryQuerySet, CommentQuerySet, PostQuerySet


class PostManager(models.Manager.from_queryset(PostQuerySet)):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).select_related(
            'author', 'category', 'location'
        )


class CommentManager(models.Manager.from_queryset(CommentQuerySet)):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db).select_related(
            'author', 'post'
        )


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
