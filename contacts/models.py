from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    faculty = models.CharField(
        max_length=100,
        verbose_name="Факультет"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )
    message = models.TextField(
        verbose_name="Примечание"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"

    def __str__(self):
        return f"{self.name} - {self.faculty}"


class ContactFormConfig(models.Model):
    form_title = models.JSONField(
        default=dict,
        verbose_name="Заголовок формы"
    )
    form_description = models.JSONField(
        default=dict,
        verbose_name="Описание формы"
    )
    label_name = models.JSONField(
        default=dict,
        verbose_name="Label: Имя"
    )
    label_faculty = models.JSONField(
        default=dict,
        verbose_name="Label: Факультет"
    )
    label_phone = models.JSONField(
        default=dict,
        verbose_name="Label: Телефон"
    )
    label_message = models.JSONField(
        default=dict,
        verbose_name="Label: Примечание"
    )
    placeholder_name = models.JSONField(
        default=dict,
        verbose_name="Placeholder: Имя"
    )
    placeholder_faculty = models.JSONField(
        default=dict,
        verbose_name="Placeholder: Факультет"
    )
    placeholder_phone = models.JSONField(
        default=dict,
        verbose_name="Placeholder: Телефон"
    )
    placeholder_message = models.JSONField(
        default=dict,
        verbose_name="Placeholder: Примечание"
    )
    faculty_options = models.JSONField(
        default=list,
        verbose_name="Опции факультетов"
    )
    submit_button_text = models.JSONField(
        default=dict,
        verbose_name="Текст кнопки отправки"
    )
    success_message = models.JSONField(
        default=dict,
        verbose_name="Сообщение об успехе"
    )
    error_message = models.JSONField(
        default=dict,
        verbose_name="Сообщение об ошибке"
    )
    validation_name_min_length = models.JSONField(
        default=dict,
        verbose_name="Ошибка: имя слишком короткое"
    )
    validation_message_min_length = models.JSONField(
        default=dict,
        verbose_name="Ошибка: сообщение слишком короткое"
    )
    validation_phone_invalid = models.JSONField(
        default=dict,
        verbose_name="Ошибка: невалидный телефон"
    )
    validation_faculty_required = models.JSONField(
        default=dict,
        verbose_name="Ошибка: факультет обязателен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Конфигурация формы обратной связи"
        verbose_name_plural = "Конфигурация формы обратной связи"

    def __str__(self):
        return "Конфигурация формы обратной связи"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'ContactFormConfig':
        obj, created = cls.objects.get_or_create(pk=1)
        return obj