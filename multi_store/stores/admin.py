from django.contrib import admin, messages

# Register your models here.
from django.db.models import ProtectedError

from .models import AttributeKey, Store, StoreAttribute


@admin.register(AttributeKey)
class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ('key_name', 'attribute_type')

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ProtectedError:
            self.message_user(request, f"无法删除 '{obj.key_name}'，因为它被使用了。", level=messages.ERROR)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'store_address', 'store_manager')

@admin.register(StoreAttribute)
class StoreAttributeAdmin(admin.ModelAdmin):
    list_display = ('store', 'attribute_key', 'get_attribute_value')
    list_filter = ('attribute_key',)
    readonly_fields = ('get_attribute_value',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.attribute_key:
            attribute_type = obj.attribute_key.attribute_type
            if attribute_type == AttributeKey.FILE:
                form.base_fields['attribute_file'].required = True
            elif attribute_type == AttributeKey.IMAGE:
                form.base_fields['attribute_image'].required = True
            else:
                form.base_fields['attribute_value'].required = True
        return form

    def save_model(self, request, obj, form, change):
        # Ensure only the correct field is saved based on attribute type
        attribute_type = obj.attribute_key.attribute_type
        if attribute_type == AttributeKey.FILE:
            obj.attribute_value = None
            obj.attribute_image = None
        elif attribute_type == AttributeKey.IMAGE:
            obj.attribute_value = None
            obj.attribute_file = None
        else:
            obj.attribute_file = None
            obj.attribute_image = None
        super().save_model(request, obj, form, change)