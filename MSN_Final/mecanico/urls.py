from django.urls import path
from . import  views

app_name = 'mecanico'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('insertarMantenimiento/', views.insertarMantenimiento, name='insertarMantenimiento'),
    path('modificarMantenimiento/', views.modificarMantenimiento, name='modificarMantenimiento'),
    path('modificarMantenimiento2/', views.modificarMantenimiento2, name='modificarMantenimiento'),
    path('consultarMantenimiento/', views.consultarMantenimiento, name='consultarMantenimiento'),
    path('consultarMantenimiento2/', views.consultarMantenimiento2, name='consultarMantenimiento2'),
    
    path('insertarPeritaje/', views.insertarPeritaje, name='insertarPeritaje'),
    path('modificarPeritaje/', views.modificarPeritaje, name='modificarPeritaje'),
    path('modificarPeritaje2/', views.modificarPeritaje2, name='modificarPeritaje2'),
    path('consultarPeritaje/', views.consultarPeritaje, name='consultarPeritaje'),
    path('consultarPeritaje2/', views.consultarPeritaje2, name='consultarPeritaje2'),
    
    path('insertarRepuesto/', views.insertarRepuesto, name='insertarRepuesto'),
    path('modificarRepuesto/', views.modificarRepuesto, name='modificarRepuesto'),
    path('modificarRepuesto2/', views.modificarRepuesto2, name='modificarRepuesto2'),
    path('consultarRepuesto/', views.consultarRepuesto, name='consultarRepuesto'),
    path('consultarRepuesto2/', views.consultarRepuesto2, name='consultarRepuesto2'),
]

