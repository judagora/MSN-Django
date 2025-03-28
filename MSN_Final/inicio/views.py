from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import RegistroForm, LoginForm
from .models import Usuario, Cliente
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import random
from django.contrib import messages


# Variable global temporal para almacenar códigos (en producción usa cache o base de datos)
temp_codes = {}

def password_reset_request(request):

    storage = messages.get_messages(request)
    list(storage)

    if request.method == "POST":
        email = request.POST.get('email')
        if Usuario.objects.filter(correo_electronico=email).exists():
            user = Usuario.objects.get(correo_electronico=email)
            
            # Generar código de 5 dígitos
            code = str(random.randint(10000, 99999))
            temp_codes[email] = {
                'code': code,
                'user_id': user.id_usuario
            }
            
            # Enviar correo con el código
            subject = "🔑 Código de Verificación - Motors Safety Net 🔑"

            message = f"""
            ============================================
            🛡️ VERIFICACIÓN DE SEGURIDAD 🛡️
            ============================================

            Hola {user.nombres},

            Has solicitado restablecer tu contraseña en Motors Safety Net.

            📌 TU CÓDIGO DE VERIFICACIÓN:
            ----------------------------------
            🔢 {code}
            ----------------------------------

            ⏳ Este código es válido por 10 minutos.

            ⚠️ IMPORTANTE:
            - No compartas este código con nadie
            - El equipo de Motors Safety Net nunca te pedirá este código
            - Si no solicitaste este cambio, ignora este mensaje

            📬 ¿Problemas o preguntas?
            Contacta a nuestro equipo de soporte:
            ✉️ motorssafetynet@gmail.com

            ============================================
            🔧 Motors Safety Net - Tu seguridad es nuestra prioridad
            ============================================

            ℹ️ Este es un mensaje automático, por favor no responder.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return render(request, 'verify_code.html', {'email': email})
        else:
            messages.error(request, "No existe un usuario con este correo electrónico.")
    
    return render(request, 'password_reset_form.html')

def verify_code(request):

    storage = messages.get_messages(request)
    list(storage)

    if request.method == "POST":
        email = request.POST.get('email')
        user_code = request.POST.get('code')
        
        if email in temp_codes and temp_codes[email]['code'] == user_code:
            request.session['reset_email'] = email
            return render(request, 'new_password_form.html', {'email': email})
        else:
            messages.error(request, "Código incorrecto o expirado.")
            return render(request, 'verify_code.html', {'email': email})
    
    return redirect('password_reset')

def set_new_password(request):

    storage = messages.get_messages(request)
    list(storage)
    
    if request.method == "POST":
        email = request.session.get('reset_email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'new_password_form.html', {'email': email})
        
        if email in temp_codes:
            user_id = temp_codes[email]['user_id']
            user = Usuario.objects.get(id_usuario=user_id)
            
            # Actualizar contraseña
            user.password = make_password(password)
            user.save()
            
            # Limpiar código temporal
            del temp_codes[email]
            del request.session['reset_email']
            
            messages.success(request, "Contraseña actualizada correctamente. Por favor inicia sesión.")
            return render(request, 'new_password_form.html')
    
    return redirect('inicio:password_reset')


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["password1"])  # Encripta la contraseña
            usuario.save()

            if usuario.rol_usuario == "Cliente":
                Cliente.objects.create(id_usuario=usuario, estado_de_la_cuenta="ACTIVO")

            return render(request, 'register.html', {'form': RegistroForm(), 'registro_exitoso': True})  # Redirige a la página de registro con un mensaje de éxito
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistroForm()  # Se inicializa el formulario si no es POST

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            correo = form.cleaned_data['username']  # AuthenticationForm usa "username" para el correo
            password = form.cleaned_data['password']

            usuario = authenticate(request, username=correo, password=password)
            print("Usuario autenticado:", usuario)
            
            if usuario is not None:
                if not usuario.is_active:
                    messages.error(request, "Tu cuenta ha sido desactivada. Contacta con soporte para más información.")
                    return redirect('login_view')

                auth_login(request, usuario)
                print("Usuario en sesión:", request.user)
                grupo = usuario.rol_usuario  # Obtiene el primer grupo del usuario
                print("Grupo del usuario:", grupo) 

                if grupo:
                    print("Nombre del grupo:", grupo)
                    if grupo == "Cliente":
                        print("Redirigiendo a: cliente:inicio")
                        return redirect('cliente:inicio')
                    elif grupo == "Administrador":
                        return redirect('administrador:inicio')
                    elif grupo == "Mecanico":
                        return redirect('mecanico:inicio')

                messages.error(request, "No tienes permisos para acceder a esta página.")
                return redirect('login_view')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'login.html', {"form": form})
def logout_view(request):
    request.session.flush()
    return render(request, 'login.html')
