from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from inicio.models import Cliente
from inicio.models import Vehiculo
from django.contrib.auth import logout
from .forms import VehiculoForm, ClienteForm, SoatForm
from django.contrib import messages
from datetime import datetime
# Create your views here.

@login_required
def inicio(request):
    usuario = request.user

    try:
        cliente = Cliente.objects.get(id_usuario=request.user)  # Obtener el cliente vinculado al usuario
        vehiculos = Vehiculo.objects.filter(id_cliente=cliente)  # Obtener los vehículos asociados al cliente
    except Cliente.DoesNotExist:
        vehiculos = []

    return render(request, 'indexCliente.html', {'usuario': usuario, 'vehiculos': vehiculos})

@login_required
def registrovehiculo(request):
    año_actual = datetime.now().year
    try:
        cliente = Cliente.objects.get(id_usuario=request.user)  # Obtener el cliente vinculado al usuario
    except Cliente.DoesNotExist:
        messages.error(request, "No se encontró un cliente asociado a tu cuenta.")
        return redirect('cliente:inicio')
    
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.id_cliente = cliente
            vehiculo.save()
            messages.success(request, "Vehículo registrado con éxito.")
            return render(request, 'addvehiculo.html', {'form': VehiculoForm(), 'registro_exitoso': True})
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = VehiculoForm()
    return render(request, 'addvehiculo.html', {'form': form, 'año_actual': año_actual}) # Se envía el año actual para validar el modelo del vehículo


@login_required
def info_vehiculo(request, id_vehiculo):
    
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo, id_cliente__id_usuario=request.user)

    return render(request, 'vehiculo.html', {'vehiculo': vehiculo})


@login_required
def editar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    edit_exitoso = False
    if request.method == "POST":
        print(request.POST)
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente.")
            edit_exitoso = True
        else:
            print(form.errors)
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'editvehiculo.html', {'form': form, 'vehiculo': vehiculo, 'edit_exitoso': edit_exitoso})

@login_required
def eliminar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    vehiculo.delete()
    messages.success(request, "Vehículo eliminado correctamente.")
    return redirect('cliente:inicio')

@login_required
def cuenta(required):
    return render(required, 'cuenta.html')

@login_required
def editar_cuenta(request):
    usuario = request.user  # Obtener el usuario actual
    edit_exitoso = False
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=usuario)  # Se pasa el usuario en instance
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            edit_exitoso = True
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ClienteForm(instance=usuario)  # Cargar formulario con datos actuales

    return render(request, 'editarcliente.html', {'form': form, 'edit_exitoso': edit_exitoso})

@login_required
def desactivar_cuenta(request):
    usuario = request.user
    if request.method == "POST":
        usuario.is_active = False
        usuario.save()
        messages.success(request, "Cuenta desactivada correctamente.")
        logout(request)
        return redirect('login_view')
    return render (request, 'confirmar_eliminar_cuenta.html')

@login_required
def soat(request):
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first() 
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)

    if request.method == "POST":
        form = SoatForm(request.POST, cliente=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "SOAT registrado correctamente.")
            return redirect('cliente:soat')  # Cambia esto según tu estructura de URLs
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = SoatForm(cliente=cliente)
    return render(request, 'soat.html', {'form': form, 'vehiculos': vehiculos})


