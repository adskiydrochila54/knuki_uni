from rest_framework import viewsets, generics
from .models import *
from .serializers import *


class UploadsViewSet(viewsets.ModelViewSet):
    queryset = Uploads.objects.all()
    serializer_class = UploadsSerializer
