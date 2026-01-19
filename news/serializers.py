from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    lang = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "lead",
            "body",
            "slug",
            "seo_title",
            "seo_description",
            "status",
            "published_at",
            "hero_image",
            "created_at",
            "lang",
        )

    def get_lang(self, obj):
        return self.context.get("lang", "ky")

    def validate(self, attrs):
        title = attrs.get("title", {})
        body = attrs.get("body", {})

        if "ky" not in title or "ky" not in body:
            raise serializers.ValidationError("Кыргызский язык обязателен")

        return attrs