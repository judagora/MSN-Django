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
]

