from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    topic = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Тема"
    )
    message = models.TextField(
        verbose_name="Сообщение"
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
        return f"{self.name} <{self.email}>"
