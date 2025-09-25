from django.contrib.auth import get_user_model
from django.db import models

from core.constants import FIELDS_MAX_LENGTH, STR_LENGTH
from core.models import PublishedAndCreatedAt

User = get_user_model()

class Category(PublishedAndCreatedAt):
    title = models.CharField('Заголовок', max_length=FIELDS_MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.',
        unique=True
    )
    class Meta(PublishedAndCreatedAt.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:STR_LENGTH]


class Location(PublishedAndCreatedAt):
    name = models.CharField('Название места', max_length=FIELDS_MAX_LENGTH)

    class Meta(PublishedAndCreatedAt.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:STR_LENGTH]


class Post(PublishedAndCreatedAt):
    title = models.CharField('Заголовок', max_length=FIELDS_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return self.title[:STR_LENGTH]
