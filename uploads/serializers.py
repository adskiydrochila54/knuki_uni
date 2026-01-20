from rest_framework import serializers
from .models import Uploads


class UploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploads
        fields = ['id', 'filename', 'user', 'file_type', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']

    # Проверка загружаемого файла
    def validate_file(self, value):
        # 1. Проверяем размер файла (максимум 5 МБ)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("Файл слишком большой. Максимум 5 МБ.")

        # 2. Проверяем расширение файла
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Недопустимый формат файла. Разрешено: {', '.join(allowed_extensions)}")

        return value
