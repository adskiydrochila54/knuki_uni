from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import ContactMessage, ContactFormConfig
from .serializers import (
    ContactMessageSerializer,
    ContactMessageReadSerializer,
    ContactMessageListSerializer,
    ContactFormConfigSerializer,
)
from .throttles import ContactRateThrottle


@extend_schema(
    tags=["Contacts"],
    summary="Получить конфигурацию формы обратной связи",
    description="Возвращает все UI-тексты формы на текущем языке (Accept-Language)",
)
class ContactFormConfigView(generics.RetrieveAPIView):
    serializer_class = ContactFormConfigSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return ContactFormConfig.load()


@extend_schema(
    tags=["Contacts"],
    summary="Отправка сообщения обратной связи",
    description="Публичный эндпоинт для отправки сообщения. Ограничен rate-limit.",
)
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    throttle_classes = [ContactRateThrottle]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        config = ContactFormConfig.load()
        success_field_data = config.success_message

        language_code = getattr(request, 'LANGUAGE_CODE', 'ky')
        success_message = success_field_data.get(
            language_code,
            success_field_data.get('ky', 'Success')
        )

        return Response(
            {
                'message': success_message,
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Contacts"],
    summary="Список сообщений обратной связи",
    description="Доступно только администраторам",
    parameters=[
        OpenApiParameter(
            name="unread",
            type=bool,
            required=False,
            description="Показать только непрочитанные сообщения",
        )
    ],
)
class ContactMessageListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("unread") == "true":
            qs = qs.filter(is_read=False)
        return qs


@extend_schema(
    tags=["Contacts"],
    summary="Отметить сообщение как прочитанное",
    description="Помечает сообщение как прочитанное. Тело запроса не требуется.",
    request=None,
)
class ContactMessageReadView(generics.UpdateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageReadSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(is_read=True)