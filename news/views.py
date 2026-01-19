from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .models import News
from .serializers import NewsSerializer

def get_lang(request):
    return request.GET.get('lang') or request.headers.get('Accept-Language', 'ky').split(',')[0][:2]

LANG_PARAM = OpenApiParameter(
    name='lang',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Язык контента (ky, ru, en). По умолчанию ky.',
    required=False,
)

class NewsListAPIView(ListAPIView):
    serializer_class = NewsSerializer

    @extend_schema(
        summary="Список опубликованных новостей",
        parameters=[LANG_PARAM],
        responses={200: NewsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return News.objects.filter(status='published')

    def get_serializer_context(self):
        return {'lang': get_lang(self.request)}


class NewsDetailAPIView(RetrieveAPIView):
    serializer_class = NewsSerializer

    @extend_schema(
        summary="Детальный просмотр новости по слагу",
        parameters=[LANG_PARAM],
        responses={200: NewsSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        slug_value = self.kwargs.get("slug")
        lang = get_lang(self.request)
        queryset = News.objects.filter(status='published')

        filter_kwargs = {f"slug__{lang}": slug_value}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

    def get_serializer_context(self):
        return {'lang': get_lang(self.request)}


class NewsCreateAPIView(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Создание новой новости (Админ)",
        description="Кыргызский язык обязателен. Остальные будут переведены автоматически.",
        request=NewsSerializer,
        responses={201: NewsSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class NewsAdminDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    @extend_schema(summary="Управление новостью по ID (Админ)")
    def get(self, request, *args, kwargs): return super().get(request, *args, kwargs)

    @extend_schema(summary="Полное обновление новости (Админ)")
    def put(self, request, *args, kwargs): return super().put(request, *args, kwargs)

    @extend_schema(summary="Частичное обновление новости (Админ)")
    def patch(self, request, *args, kwargs): return super().patch(request, *args, kwargs)

    @extend_schema(summary="Удаление новости (Админ)")
    def delete(self, request, *args, kwargs): return super().delete(request, *args, kwargs)

    def get_serializer_context(self):
        return {'lang': get_lang(self.request)}
