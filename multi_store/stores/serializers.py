from rest_framework import serializers
from django.db.models import QuerySet

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        store_id = None

        # 如果 context 中有 store_id，使用它
        if 'store_id' in self.context:
            store_id = self.context['store_id']

        # 如果实例是单个对象而不是 QuerySet
        if self.instance and not isinstance(self.instance, list) and not isinstance(self.instance, QuerySet):
            store_id = self.instance.store_id

        # 根据 store_id 过滤 attribute_key
        if store_id:
            self.fields['attribute_key'].queryset = AttributeKey.objects.exclude(
                id__in=StoreAttribute.objects.filter(store_id=store_id).values_list('attribute_key_id', flat=True)
            )
            
class StoreSerializer(serializers.ModelSerializer):
    attributes = StoreAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'