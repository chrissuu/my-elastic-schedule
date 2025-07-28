from rest_framework import viewsets
from .models import BlobModel
from .serializers import BlobSerializer

class BlobViewSet(viewsets.ModelViewSet):
    queryset = BlobModel.objects.all()
    serializer_class = BlobSerializer