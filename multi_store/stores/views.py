from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Store, StoreAttribute, AttributeKey
from .serializers import StoreSerializer, StoreAttributeSerializer, AttributeKeySerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class AttributeKeyViewSet(viewsets.ModelViewSet):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer

class StoreAttributeViewSet(viewsets.ModelViewSet):
    queryset = StoreAttribute.objects.all()
    serializer_class = StoreAttributeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        store_id = self.request.data.get('store') or self.request.query_params.get('store')
        if store_id:
            context['store_id'] = store_id
        return context