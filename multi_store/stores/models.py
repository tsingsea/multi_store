from django.db import models

# Create your models here.

class Store(models.Model):
    store_name = models.CharField(max_length=255)
    store_address = models.TextField(blank=True, null=True)
    store_manager = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.store_name

# 存储所有可能的attribute_key。通过外键将它们与StoreAttribute关联。这样，每次创建新的StoreAttribute时，只能从已有的attribute_key中选择。
class AttributeKey(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    DATETIME = 'datetime'
    BOOLEAN = 'boolean'
    JSON = 'json'
    FILE = 'file'
    IMAGE = 'image'

    ATTRIBUTE_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (DATE, 'Date'),
        (DATETIME, 'Datetime'),
        (BOOLEAN, 'Boolean'),
        (JSON, 'JSON'),
        (FILE, 'File'),
        (IMAGE, 'Image'),
    ]

    key_name = models.CharField(max_length=255, unique=True)
    attribute_type = models.CharField(
        max_length=50,
        choices=ATTRIBUTE_TYPE_CHOICES,
        default=TEXT
    )

    def __str__(self):
        return f"{self.key_name} ({self.get_attribute_type_display()})"

class StoreAttribute(models.Model):
    store = models.ForeignKey(Store, related_name='attributes', on_delete=models.CASCADE)
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.PROTECT)
    attribute_value = models.TextField(blank=True, null=True)  # 用于存储非文件的值
    attribute_file = models.FileField(upload_to='store_files/', blank=True, null=True)  # 用于存储文件
    attribute_image = models.ImageField(upload_to='store_images/', blank=True, null=True)  # 用于存储图片

    def __str__(self):
        return f"{self.attribute_key.key_name}: {self.get_attribute_value()}"

    def get_attribute_value(self):
        if self.attribute_key.attribute_type == AttributeKey.FILE:
            return self.attribute_file.url if self.attribute_file else None
        elif self.attribute_key.attribute_type == AttributeKey.IMAGE:
            return self.attribute_image.url if self.attribute_image else None
        else:
            return self.attribute_value