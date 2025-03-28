from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
import os

# Señal para crear admin por defecto
@receiver(post_migrate)
def crear_admin_por_defecto(sender, **kwargs):
    # Verificar que la señal venga de la app correcta
    if sender.name == 'inicio':
        try:
            # Obtener los modelos
            Usuario = apps.get_model('inicio', 'Usuario')
            Administrador = apps.get_model('inicio', 'Administrador')
            
            # Verificar si ya existe un administrador
            if not Usuario.objects.filter(rol_usuario='Administrador').exists():
                # Crear el superusuario (sin rol_usuario aquí)
                admin_user = Usuario.objects.create_superuser(
                    correo_electronico=os.getenv('DEFAULT_ADMIN_EMAIL', 'motorssafetynet@gmail.com'),
                    nombre_usuario=os.getenv('DEFAULT_ADMIN_USERNAME', 'MotorsSN'),
                    contraseña=os.getenv('DEFAULT_ADMIN_PASSWORD', 'msn123456'),
                    nombres='Administrador',
                    apellidos='Sistema',
                    telefono='3203091045',
                    is_staff=True,
                    is_active=True
                )
                
                # Actualizar el rol específicamente
                admin_user.rol_usuario = 'Administrador'
                admin_user.save()
                
                # Crear el registro en Administrador
                Administrador.objects.create(
                    ubicacion=os.getenv('DEFAULT_ADMIN_LOCATION', 'Sede Principal'),
                    id_usuario=admin_user
                )
                
                # Mensaje de confirmación
                print("\n" + "="*50)
                print("¡Administrador por defecto creado exitosamente!")
                print(f"Email: {admin_user.correo_electronico}")
                print(f"Usuario: {admin_user.nombre_usuario}")
                print("="*50 + "\n")
                
        except Exception as e:
            print("\n" + "!"*50)
            print(f"Error al crear admin por defecto: {str(e)}")
            print("!"*50 + "\n")