
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('administrador/', include('administrador.urls')),
    path('', include('inicio.urls')),
    path('cliente/', include('cliente.urls')),
    path('mecanico/', include('mecanico.urls')),
    path('admin/', admin.site.urls),
]
