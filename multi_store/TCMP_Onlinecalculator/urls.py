# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('success/', views.success, name='success'),
    path('calculate/', views.calculate_price, name='calculate_price'),
    path('search-medicine/', views.search_medicine, name='search_medicine'),
    path('clear/', views.clear_calculations, name='clear_calculations'),
]
