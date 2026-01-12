from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'topic', 'message')

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "Имя не может быть короче 2 символов"
            )
        return value

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Сообщение слишком короткое"
            )
        return value


class ContactMessageReadSerializer(serializers.ModelSerializer):
    """
    Используется ТОЛЬКО для пометки сообщения как прочитанного
    """
    class Meta:
        model = ContactMessage
        fields = ()
