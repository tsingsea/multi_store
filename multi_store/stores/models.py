from django.db import models

# Create your models here.

class Store(models.Model):
    store_name = models.CharField(max_length=255)
    store_address = models.TextField(blank=True, null=True)
    store_manager = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.store_name

class StoreAttribute(models.Model):
    store = models.ForeignKey(Store, related_name='attributes', on_delete=models.CASCADE)
    attribute_key = models.CharField(max_length=255)
    attribute_value = models.TextField()
    attribute_type = models.CharField(max_length=50, default='text')  # 'text', 'number', 'date', 'json', etc.

    def __str__(self):
        return f"{self.attribute_key}: {self.attribute_value}"
