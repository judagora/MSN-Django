from django.urls import path
from . import views
app_name = 'administrador'


urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('modificarMecanico/', views.modificarMecanico, name='modificarMecanico'),
    path('insertarMecanico/', views.insertarMecanico, name='insertarMecanico'),
    path('mecanicos/', views.mecanicos, name='mecanicos'),
    path('mantenimientos/', views.mantenimientos, name='mantenimientos'),
    path('historialesVehiculo/', views.historialesVehiculo, name='historialesVehiculo'),
    path('talleresMecanico/', views.talleresMecanico, name='talleresMecanico'),
    path('insertarMantenimiento/', views.insertarMantenimiento, name='insertarMantenimiento'),
    path('insertarTaller/', views.peritajes, name='peritajes'),
    path('modificarPeritaje/', views.modificarPeritaje, name='modificarPeritaje'),
    path('modificarMantenimiento/', views.modificarMantenimiento, name='modificarMantenimiento'),
    path('peritajes/', views.peritajes, name='peritajes'),
    path('modificarTaller/', views.modificarTaller, name='modificarTaller'),

]