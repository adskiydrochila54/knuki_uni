from django.urls import path
from .views import NewsListAPIView, NewsCreateAPIView, NewsDetailAPIView, NewsAdminDetailAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = (
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #Public
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('news/<str:slug>/', NewsDetailAPIView.as_view(), name='news-detail'),
    #Admin
    path('admin/news/', NewsCreateAPIView.as_view(), name='news-create'),
    path('admin/news/<int:pk>/', NewsAdminDetailAPIView.as_view(), name= 'news-admin-detail')
)