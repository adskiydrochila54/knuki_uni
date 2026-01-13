from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Uploads(models.Model):
    filename = models.CharField(max_length=64, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    FILE_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('other', 'Other'),
    )
    file_type = models.CharField(max_length=16, choices=FILE_TYPES, default='other')
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            self.type = self.get_file_type()
        super().save(*args, **kwargs)

    def get_file_type(self):
        name = self.file.name.lower()
        if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return 'image'
        if name.endswith(('.mp4', '.mov', '.avi')):
            return 'video'
        if name.endswith('.pdf'):
            return 'pdf'
        return 'other'

    @property
    def url(self):
        return self.file.url

    def __str__(self):
        return f'{self.file.name}'
