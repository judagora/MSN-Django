from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import RegistroForm, LoginForm
from .models import Usuario, Cliente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib import messages


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
                        return redirect('administrador:index')
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
    return redirect('login')
