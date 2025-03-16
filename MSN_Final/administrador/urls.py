from django.urls import path
from . import views
app_name = 'administrador'


urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('modificarMecanico/<int:id_usuario>/', views.modificarMecanico, name='modificarMecanico'),
    path('eliminar_mecanico/<int:id_usuario>/', views.eliminar_mecanico, name='eliminar_mecanico'),
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