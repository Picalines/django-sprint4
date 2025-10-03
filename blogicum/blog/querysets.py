from django.db import models
from django.utils.timezone import now


class PostQuerySet(models.QuerySet):
    def of_author(self, user):
        return self.filter(author__username=user.username)

    def _public_q(self):
        return models.Q(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        )

    def public(self):
        return self.filter(self._public_q())

    def visible_for(self, user):
        return self.filter(
            models.Q(author__username=user.username) | self._public_q()
        )

    def from_old_to_new(self):
        return self.order_by('-pub_date')

    def with_comment_counts(self):
        return self.annotate(comment_count=models.Count('comments'))


class CommentQuerySet(models.QuerySet):
    def of_post(self, post):
        return self.filter(post__pk=post.pk)


class CategoryQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_published=True)
