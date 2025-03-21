from django.urls import path
from . import views

app_name = 'administrador'


urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('cambiar-contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('modificarMecanico/<int:id_usuario>/', views.modificarMecanico, name='modificarMecanico'),
    path('eliminar_mecanico/<int:id_usuario>/', views.eliminar_mecanico, name='eliminar_mecanico'),
    path('insertarMecanico/', views.insertarMecanico, name='insertarMecanico'),
    path('mecanicos/', views.mecanicos, name='mecanicos'),
    path('mantenimientos/', views.mantenimientos, name='mantenimientos'),
    path('historialesVehiculo/', views.historialesVehiculo, name='historialesVehiculo'),
    path('talleresMecanico/', views.talleresMecanico, name='talleresMecanico'),
    path('insertarTaller/', views.insertarTaller, name='insertarTaller'),
    path('modificarMantenimiento/<int:id_mantenimiento>/', views.modificarMantenimiento, name='modificarMantenimiento'),
    path('peritajes/', views.peritajes, name='peritajes'),
    path('modificarPeritaje/<int:id_peritaje>/', views.modificarPeritaje, name='modificarPeritaje'),
    path('modificarTaller/<int:id_taller_mecanico>/', views.modificarTaller, name='modificarTaller'),
    path('eliminarMantenimiento/<int:id_mantenimiento>/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
    path('eliminarTaller/<int:id_taller_mecanico>/', views.eliminarTaller, name='eliminar_taller'),
    path('eliminarPeritaje/<int:id_peritaje>/', views.eliminarPeritaje, name='eliminar_peritaje'),



]