from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('inventory/<str:id>/', views.inventory, name='inventory'),
    path('add-inventory/', views.add_inventory, name='add_inventory'),
    path('calculate-inventory/', views.calculate_inventory, name='calculate_inventory'),
    path('update_parameters/', views.update_parameters, name='update_parameters'),
]
