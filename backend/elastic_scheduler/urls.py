from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlobViewSet

router = DefaultRouter()
router.register(r"blobs", BlobViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
