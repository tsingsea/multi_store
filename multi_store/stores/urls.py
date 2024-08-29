from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StoreViewSet, StoreAttributeViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'attributes', StoreAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]