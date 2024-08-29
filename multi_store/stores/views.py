from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Store, StoreAttribute
from .serializers import StoreSerializer, StoreAttributeSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreAttributeViewSet(viewsets.ModelViewSet):
    queryset = StoreAttribute.objects.all()
    serializer_class = StoreAttributeSerializer