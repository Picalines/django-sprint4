from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from core.constants import FIELDS_MAX_LENGTH, STR_LENGTH

User = get_user_model()


class PublishedAndCreatedAt(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('created_at',)


class CategoryQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_published=True)


class Category(PublishedAndCreatedAt):
    objects = CategoryQuerySet.as_manager()

    title = models.CharField("Заголовок", max_length=FIELDS_MAX_LENGTH)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        help_text="Идентификатор страницы для URL; разрешены символы "
        "латиницы, цифры, дефис и подчёркивание.",
        unique=True,
    )

    class Meta(PublishedAndCreatedAt.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title[:STR_LENGTH]


class Location(PublishedAndCreatedAt):
    name = models.CharField("Название места", max_length=FIELDS_MAX_LENGTH)

    class Meta(PublishedAndCreatedAt.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self) -> str:
        return self.name[:STR_LENGTH]


class PostQuerySet(models.QuerySet):
    def of_author(self, user):
        return self.select_related('author').filter(
            author__username=user.username
        )

    def _public_q(self):
        return models.Q(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        )

    def public(self):
        return self.select_related('category').filter(self._public_q())

    def visible_for(self, user):
        return self.select_related('author', 'category').filter(
            models.Q(author__username=user.username) | self._public_q()
        )

    def from_old_to_new(self):
        return self.order_by('-pub_date')

    def with_comment_counts(self):
        return self.annotate(comment_count=models.Count('comments'))


class Post(PublishedAndCreatedAt):
    objects = PostQuerySet.as_manager()

    title = models.CharField("Заголовок", max_length=FIELDS_MAX_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )
    image = models.ImageField('Изображение', blank=True)

    class Meta:
        default_related_name = "posts"
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.title[:STR_LENGTH]


class CommentQuerySet(models.QuerySet):
    def of_post(self, post: Post):
        return self.select_related('post').filter(post__pk=post.pk)


class Comment(PublishedAndCreatedAt):
    objects = CommentQuerySet.as_manager()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Пост'
    )
    text = models.TextField('Текст')

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ("created_at",)
