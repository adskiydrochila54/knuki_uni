from django.urls import path

from .views import (
    ContactMessageCreateView,
    ContactMessageListView,
    ContactMessageReadView,
)

urlpatterns = [
    path(
        "create/",
        ContactMessageCreateView.as_view(),
        name="contact-create",
    ),
    path(
        "list/",
        ContactMessageListView.as_view(),
        name="contact-list",
    ),
    path(
        "<int:pk>/read/",
        ContactMessageReadView.as_view(),
        name="contact-read",
    ),
]
