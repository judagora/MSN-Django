from django.urls import path
from . import  views

app_name = 'cliente'

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
]

