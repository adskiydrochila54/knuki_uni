from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # Публичные эндпоинты
    path(
        'form-config/',
        views.ContactFormConfigView.as_view(),
        name='form-config'
    ),
    path(
        'messages/',
        views.ContactMessageCreateView.as_view(),
        name='message-create'
    ),

    # Админские эндпоинты
    path(
        'admin/messages/',
        views.ContactMessageListView.as_view(),
        name='message-list'
    ),
    path(
        'admin/messages/<int:pk>/read/',
        views.ContactMessageReadView.as_view(),
        name='message-read'
    ),
]