from rest_framework import serializers
from typing import Dict, Any, Optional


class LocalizedJSONField(serializers.Field):
    default_language = 'ky'
    supported_languages = ['ky', 'ru', 'en']

    def __init__(self, **kwargs):
        self.write_as_dict = kwargs.pop('write_as_dict', False)
        super().__init__(**kwargs)

    def to_representation(self, value: Dict[str, str]) -> str:
        if not isinstance(value, dict):
            return str(value) if value else ""

        request = self.context.get('request')
        language_code = getattr(request, 'LANGUAGE_CODE', self.default_language)

        return value.get(
            language_code,
            value.get(self.default_language, "")
        )

    def to_internal_value(self, data: Any) -> Dict[str, str]:
        if self.write_as_dict and isinstance(data, dict):
            if not all(key in self.supported_languages for key in data.keys()):
                raise serializers.ValidationError(
                    f"Supported languages: {', '.join(self.supported_languages)}"
                )
            return data

        if isinstance(data, str):
            return {lang: data for lang in self.supported_languages}

        raise serializers.ValidationError(
            "Expected a string or dict with translations"
        )