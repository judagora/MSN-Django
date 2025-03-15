from django.urls import path
from . import  views

app_name = 'mecanico'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
]

