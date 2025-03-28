from django.apps import AppConfig


class InicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inicio'

    def ready(self):
        # Importa las señales
        import inicio.signals  # Para señales en archivo separado

