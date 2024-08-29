from rest_framework import serializers

from .models import Store, StoreAttribute

class StoreAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAttribute
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    attributes = StoreAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'