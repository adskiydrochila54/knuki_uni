from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_title_ky",
        "status",
        "published_at",
        "created_at",
    )

    list_filter = (
        "status",
        "published_at",
    )

    search_fields = (
        "title__ky",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Кыргызский контент (обязательно)", {
            "fields": (
                "title",
                "lead",
                "body",
            ),
            "description": "Введите минимум кыргызскую версию. Остальные языки будут добавлены автоматически.",
        }),
        ("SEO", {
            "fields": (
                "seo_title",
                "seo_description",
            )
        }),
        ("Публикация", {
            "fields": (
                "status",
                "published_at",
                "hero_image",
            )
        }),
        ("Служебная информация", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    formfield_overrides = {
        models.JSONField: {
            "widget": Textarea(attrs={"rows": 4, "cols": 60})
        }
    }

    def get_title_ky(self, obj):
        return obj.title.get("ky", "—")

    get_title_ky.short_description = "Заголовок (ky)"