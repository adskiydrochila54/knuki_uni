from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser


@extend_schema(
    tags=["Uploads"],
    summary="Upload file",
    description="Upload a file using multipart/form-data",

)
class UploadsViewSet(viewsets.ModelViewSet):
    queryset = Uploads.objects.all()
    serializer_class = UploadsSerializer


@extend_schema(
    tags=["Uploads"],
    summary="Upload file",
    description="Upload a file using multipart/form-data",

)
class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
