from core.constants import FIELDS_MAX_LENGTH, STR_LENGTH
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

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


class Category(PublishedAndCreatedAt):
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


class Post(PublishedAndCreatedAt):
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

    @staticmethod
    def of_author(posts: models.QuerySet, user):
        return posts.select_related('author').filter(
            author__username=user.username
        )

    @staticmethod
    def public(posts: models.QuerySet):
        return posts.select_related("author", "category", "location").filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        )

    @staticmethod
    def with_comment_counts(posts: models.QuerySet):
        return posts.annotate(comment_count=models.Count('comments'))


class Comment(PublishedAndCreatedAt):
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

    @staticmethod
    def of_post(comments: models.QuerySet, post: Post):
        return comments.select_related('post').filter(post__pk=post.pk)
