from rest_framework import viewsets, generics
from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser


class UploadsViewSet(viewsets.ModelViewSet):
    queryset = Uploads.objects.all()
    serializer_class = UploadsSerializer


class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
