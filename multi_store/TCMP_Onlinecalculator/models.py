from django.db import models


# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=255, verbose_name="通用名")
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="销售金额")
    sales_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="销售数量")

    def __str__(self):
        return self.name
