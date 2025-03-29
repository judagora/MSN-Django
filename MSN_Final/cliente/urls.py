from django.urls import path
from . import  views

app_name = 'cliente'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('registrovehiculo/', views.registrovehiculo, name='registrovehiculo'),
    path('info_vehiculo/<int:id_vehiculo>', views.info_vehiculo, name='vehiculo'),
    path('editar_vehiculo/<int:id_vehiculo>', views.editar_vehiculo, name='editar_vehiculo'),
    path('eliminar_vehiculo/<int:id_vehiculo>', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('cuenta/', views.cuenta, name='cuenta'),
    path('editar_cuenta/', views.editar_cuenta, name='editar_cuenta'),
    path('desactivar_cuenta/', views.desactivar_cuenta, name='desactivar_cuenta'),
    path('soat/', views.soat, name='soat'),
    path('editar_soat/<int:id_soat>', views.editar_soat, name='editar_soat'),
    path('eliminar_soat/<int:id_soat>', views.eliminar_soat, name='eliminar_soat'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('editar_notificacion/<int:id_notificacion>', views.edit_notificacion, name='editar_notificacion'),
    path('eliminar_notificacion/<int:id_notificacion>', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('mantenimiento/', views.mantenimiento, name='mantenimiento'),
    path('obtener-mecanicos/', views.obtener_mecanicos, name='obtener_mecanicos'),
    path('editar_mantenimiento/<int:id_mantenimiento>', views.editar_mantenimiento, name='editar_mantenimiento'),
    path('eliminar_mantenimiento/<int:id_mantenimiento>', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
    
]

