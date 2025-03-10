from django.urls import path
from . import views

urlpatterns = [
    path('insertarMecanico/', views.insertarMecanico, name='insertarMecanico'),
    path('mecanicos/', views.mecanicos, name='mecanicos'),
    path('mantenimientos/', views.mantenimientos, name='mantenimientos'),
    path('historialesVehiculo/', views.historialesVehiculo, name='historialesVehiculo'),
    path('talleresMecanico/', views.talleresMecanico, name='talleresMecanico'),
    path('peritajes/', views.peritajes, name='peritajes'),
]