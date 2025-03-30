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
    path('insertarTaller/', views.insertarTaller, name='insertarTaller'),
    path('peritajes/', views.peritajes, name='peritajes'),
    path('modificarTaller/<int:id_taller_mecanico>/', views.modificarTaller, name='modificarTaller'),
    path('eliminarTaller/<int:id_taller_mecanico>/', views.eliminarTaller, name='eliminar_taller'),



]