from django.urls import path
from . import  views


app_name = 'mecanico'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('insertarMantenimientoMc/', views.insertarMantenimientoMc, name='insertarMantenimientoMc'),
    path('modificarMantenimientoMc/', views.modificarMantenimientoMc, name='modificarMantenimientoMc'),
    path('modificarMantenimientoMc2/<str:placa>/<int:id_mantenimiento>/', views.modificarMantenimientoMc2, name='modificarMantenimientoMc2'),
    path('consultar-mantenimiento/', views.consultarMantenimientoMc, name='consultarMantenimientoMc'),
    path('consultar-mantenimiento/<str:placa>/', views.consultarMantenimientoMc2, name='consultarMantenimientoMc2'),
    
    
    
    path('insertarPeritajeMc/', views.insertarPeritajeMc, name='insertarPeritajeMc'),
    path('modificarPeritajeMc/', views.modificarPeritajeMc, name='modificarPeritajeMc'),
    path('modificarPeritajeMc2/<str:placa>/<int:id_peritaje>/', views.modificarPeritajeMc2, name='modificarPeritajeMc2'),
    path('consultarPeritajeMc/', views.consultarPeritajeMc, name='consultarPeritajeMc'),
    path('consultarPeritajeMc2/<str:placa>/', views.consultarPeritajeMc2, name='consultarPeritajeMc2'),
    
    path('insertarRepuestoMc/', views.insertarRepuestoMc, name='insertarRepuestoMc'),
    path('modificarRepuestoMc/', views.modificarRepuestoMc, name='modificarRepuestoMc'),
    path('modificarRepuestoMc2/<str:placa>/<int:id_repuesto>/', views.modificarRepuestoMc2, name='modificarRepuestoMc2'),
    path('consultarRepuestoMc/', views.consultarRepuestoMc, name='consultarRepuestoMc'),
    path('consultarRepuestoMc2/<str:placa>/', views.consultarRepuestoMc2, name='consultarRepuestoMc2'),
    
    
    path('verificar-placa/', views.verificar_placa, name='verificar_placa'),
    
    
    path('consultarCitaMc/', views.consultarCitaMc, name='consultarCitaMc'),
    
 
]

