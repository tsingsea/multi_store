# Register your models here.
from django.contrib import admin

from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    # 定义在列表视图中显示的字段
    list_display = ('name', 'sales_amount', 'sales_quantity')
    # 添加搜索框，支持根据通用名搜索
    search_fields = ('name',)
    # 允许过滤的字段
    list_filter = ('name',)
    # 设置可以点击排序的字段
    ordering = ('name',)
    # 设置在新增或编辑时显示的字段
    fields = ('name', 'sales_amount', 'sales_quantity')
