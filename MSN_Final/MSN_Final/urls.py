
from django.urls import path, include

urlpatterns = [
    path('administrador/', include('administrador.urls')),
    path('', include('inicio.urls')),
    path('cliente/', include('cliente.urls')),
    path('mecanico/', include('mecanico.urls')),
]
