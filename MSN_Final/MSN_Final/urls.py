
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('administrador.urls')),
    path('mecanico/', include('mecanico.urls')),
    path('', include('inicio.urls')),
    path('cliente/', include('cliente.urls')),
]
