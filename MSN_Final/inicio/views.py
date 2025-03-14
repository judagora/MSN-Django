from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .models import Usuario
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
            return render(request, 'register.html', {'form': RegistroForm(), 'registro_exitoso': True})  # Redirige a la página de registro con un mensaje de éxito
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistroForm()  # Se inicializa el formulario si no es POST

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            corrreo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            user = authenticate(correo_electronico=corrreo, password=password)

            if user is not None:
                login(request, user)

                if user.groups.filter(name="Cliente").exists():
                    return redirect('cliente:inicio')
                elif user.groups.filter(name="Administrador").exists():
                    return redirect('administrador:index')
                elif user.groups.filter(name="Mecanico").exists():
                    return redirect('mecanico:inicio')
                else:
                    return messages.error(request, "No tienes permisos para acceder a esta página.")
            else:
                form.add_error(None, "Correo o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'login.html',{"form": form})

def logout_view(request):
    request.session.flush()
    return redirect('login')
