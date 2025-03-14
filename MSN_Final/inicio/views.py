from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .models import Usuario
from django.contrib.auth.hashers import make_password
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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            correo_electronico = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            usuario = authenticate(correo_electronico=correo_electronico, password=password)
            if usuario is not None:
                login(request, usuario)
                
                if usuario.groups.filter(name='Administrador').exists():
                    return redirect('administrador:index')
                elif usuario.groups.filter(name='Mecanico').exists():
                    return redirect('mecanico:index')
                elif usuario.groups.filter(name='Cliente').exists():
                    return redirect('cliente:index')
                else:
                    messages.error(request, "Usuario o contraseña incorrectos.")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')
