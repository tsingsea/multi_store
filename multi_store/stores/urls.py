from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StoreViewSet, StoreAttributeViewSet, AttributeKeyViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'attributes', StoreAttributeViewSet)
router.register(r'attribute-keys', AttributeKeyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]