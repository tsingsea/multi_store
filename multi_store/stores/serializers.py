from rest_framework import serializers

from .models import Store, StoreAttribute, AttributeKey


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'

class StoreAttributeSerializer(serializers.ModelSerializer):
    attribute_key = serializers.SlugRelatedField(
        queryset=AttributeKey.objects.all(),
        slug_field='key_name'
    )

    class Meta:
        model = StoreAttribute
        fields = '__all__'

    def validate(self, data):
        attribute_type = data['attribute_key'].attribute_type
        if attribute_type == AttributeKey.FILE and not data.get('attribute_file'):
            raise serializers.ValidationError("File is required for this attribute type.")
        elif attribute_type == AttributeKey.IMAGE and not data.get('attribute_image'):
            raise serializers.ValidationError("Image is required for this attribute type.")
        elif attribute_type not in [AttributeKey.FILE, AttributeKey.IMAGE] and not data.get('attribute_value'):
            raise serializers.ValidationError("Value is required for this attribute type.")
        return data

class StoreSerializer(serializers.ModelSerializer):
    attributes = StoreAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'