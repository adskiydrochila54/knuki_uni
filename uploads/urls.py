from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'uploads', UploadsViewSet, basename='uploads')

urlpatterns = [
    path("", include(router.urls)),
]
