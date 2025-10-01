from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Category, Location, Post, User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "posts_count",
    )
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    list_display_links = ("username", "id")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name")}),
    )

    @admin.display(description="Постов у пользователя")
    def posts_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("text",)
    list_display = (
        "id",
        "title",
        "author",
        "text",
        "category",
        "pub_date",
        "location",
        "is_published",
        "created_at",
    )
    list_display_links = ("title",)
    list_editable = ("category", "is_published", "location")
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "pk",
        "title",
        "description",
        "slug",
        "is_published",
        "created_at",
    )
    list_editable = ("slug", "is_published")
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("pk", "name", "is_published", "created_at")
    list_editable = ("is_published",)
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


admin.site.unregister(Group)
