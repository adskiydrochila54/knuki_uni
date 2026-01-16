from rest_framework import serializers
import re

from .models import ContactMessage, ContactFormConfig
from .fields import LocalizedJSONField


class ContactFormConfigSerializer(serializers.ModelSerializer):
    form_title = LocalizedJSONField()
    form_description = LocalizedJSONField()
    label_name = LocalizedJSONField()
    label_faculty = LocalizedJSONField()
    label_phone = LocalizedJSONField()
    label_message = LocalizedJSONField()
    placeholder_name = LocalizedJSONField()
    placeholder_faculty = LocalizedJSONField()
    placeholder_phone = LocalizedJSONField()
    placeholder_message = LocalizedJSONField()
    submit_button_text = LocalizedJSONField()
    success_message = LocalizedJSONField()
    error_message = LocalizedJSONField()
    validation_name_min_length = LocalizedJSONField()
    validation_message_min_length = LocalizedJSONField()
    validation_phone_invalid = LocalizedJSONField()
    validation_faculty_required = LocalizedJSONField()
    faculty_options = serializers.SerializerMethodField()

    class Meta:
        model = ContactFormConfig
        fields = (
            'form_title',
            'form_description',
            'label_name',
            'label_faculty',
            'label_phone',
            'label_message',
            'placeholder_name',
            'placeholder_faculty',
            'placeholder_phone',
            'placeholder_message',
            'faculty_options',
            'submit_button_text',
            'success_message',
            'error_message',
            'validation_name_min_length',
            'validation_message_min_length',
            'validation_phone_invalid',
            'validation_faculty_required',
        )

    def get_faculty_options(self, obj):
        faculty_list = obj.faculty_options
        if not isinstance(faculty_list, list):
            return []

        request = self.context.get('request')
        language_code = getattr(request, 'LANGUAGE_CODE', 'ky')

        return [
            {
                'value': item.get('value', ''),
                'label': item.get('label', {}).get(
                    language_code,
                    item.get('label', {}).get('ky', '')
                )
            }
            for item in faculty_list
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('name', 'faculty', 'phone', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ContactFormConfig.load()

    def _get_localized_text(self, field_name: str) -> str:
        field_data = getattr(self.config, field_name, {})
        if not isinstance(field_data, dict):
            return ""

        request = self.context.get('request')
        language_code = getattr(request, 'LANGUAGE_CODE', 'ky')

        return field_data.get(language_code, field_data.get('ky', ''))

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            error_message = self._get_localized_text('validation_name_min_length')
            raise serializers.ValidationError(error_message)
        return value

    def validate_faculty(self, value: str) -> str:
        value = value.strip()
        if not value:
            error_message = self._get_localized_text('validation_faculty_required')
            raise serializers.ValidationError(error_message)
        return value

    def validate_phone(self, value: str) -> str:
        value = value.strip()
        phone_pattern = re.compile(r'^\+?996\s?\d{3}\s?\d{3}\s?\d{3}$')

        if not phone_pattern.match(value):
            error_message = self._get_localized_text('validation_phone_invalid')
            raise serializers.ValidationError(error_message)
        return value

    def validate_message(self, value: str) -> str:
        value = value.strip()
        if len(value) < 10:
            error_message = self._get_localized_text('validation_message_min_length')
            raise serializers.ValidationError(error_message)
        return value


class ContactMessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ()


class ContactMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = (
            'id',
            'name',
            'faculty',
            'phone',
            'message',
            'created_at',
            'is_read',
        )
        read_only_fields = fields