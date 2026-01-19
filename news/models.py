from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .translation import auto_translate
from pytils.translit import slugify as cyrillic_slugify

class News(models.Model):
    title=models.JSONField( default=dict, verbose_name="Заголовок")
    lead = models.JSONField(default=dict, blank=True, verbose_name="Лид")
    body = models.JSONField(default=dict, verbose_name="Текст")
    slug=models.JSONField(default=dict, verbose_name="Slug")
    seo_title = models.JSONField(default=dict, blank=True, verbose_name="SEO Заголовок")
    seo_description = models.JSONField(default=dict, blank=True,  verbose_name="SEO Описание")

    STATUS_CHOICES = (
        ("draft", "Черновик"),
        ("published", "Опубликовано"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    hero_image = models.ImageField(upload_to="news/%Y/%m/%d", null=True, blank=True, verbose_name="Главное изображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at  =models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    REQUIRED_LANG = 'ky'
    LANGUAGES = ('ky', 'ru', 'en')

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def clean(self):
        if self.status == 'published':
            if not self.title or self.REQUIRED_LANG not in self.title or not self.title[self.REQUIRED_LANG]:
                raise ValidationError("Кыргызский перевод обязателен для публикации")

    def save(self, *args, **kwargs):
        for field_name in ['title', 'lead', 'body', 'seo_title', 'seo_description']:
            field_value = getattr(self, field_name)
            if isinstance(field_value, dict) and 'ky' in field_value:
                for lang in ['ru', 'en']:
                    if not field_value.get(lang):
                        field_value[lang] = auto_translate(field_value['ky'], 'ky', lang)

        # 2. Генерация слагов для всех языков
        if 'ky' in self.title:
            for lang in ['ky', 'ru', 'en']:
                if lang in self.title and not self.slug.get(lang):
                    self.slug[lang] = cyrillic_slugify(self.title[lang])

        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title.get("ky") or self.title.get("ru") or "Без названия"
