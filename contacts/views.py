from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import ContactMessage
from .serializers import (
    ContactMessageSerializer,
    ContactMessageReadSerializer,
)
from .throttles import ContactRateThrottle


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
    serializer_class = ContactMessageSerializer
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
