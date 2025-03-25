from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from inicio.models import Cliente
from inicio.models import Vehiculo, Soat, Notificaciones
from django.contrib.auth import logout
from .forms import VehiculoForm, ClienteForm, SoatForm, NotificacionForm
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now
from django.core.mail import send_mail
from .tasks import enviar_notificacion
from django.http import JsonResponse
from django.core.mail import send_mail
# Create your views here.

@login_required
def inicio(request):
    storage = messages.get_messages(request)
    list(storage)
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
    storage = messages.get_messages(request)
    list(storage)
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first() 
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)
    soats = Soat.objects.filter(id_vehiculo__id_cliente=cliente)
    registro_soat = False
    if request.method == "POST":
        form = SoatForm(request.POST, cliente=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "SOAT registrado correctamente.")
            registro_soat = True
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = SoatForm(cliente=cliente)
    return render(request, 'soat.html', {'form': form, 'vehiculos': vehiculos, 'registro_soat': registro_soat, 'soats': soats})

@login_required
def editar_soat(request, id_soat):
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first() 
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)
    soat = get_object_or_404(Soat, id_soat=id_soat)
    act_soat = False
    if request.method == "POST":
        form = SoatForm(request.POST, instance=soat)
        if form.is_valid():
            form.save()
            act_soat = True
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = SoatForm(instance=soat)
    return render(request, 'editarsoat.html', {'form': form, 'soat': soat, 'vehiculos': vehiculos, 'act_soat': act_soat})

@login_required
def eliminar_soat(request, id_soat):
    soat = get_object_or_404(Soat, id_soat=id_soat)
    soat.delete()
    messages.success(request, "SOAT eliminado correctamente.")
    return redirect('cliente:soat')


@login_required
def notificaciones(request):

    storage = messages.get_messages(request)
    list(storage)

    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first()
    notificaciones = Notificaciones.objects.filter(id_cliente=cliente)
    registro_notificacion = False
    hoy = datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        form = NotificacionForm(request.POST)
        if form.is_valid():
            notificacion = form.save(commit=False)
            notificacion.id_cliente = cliente
            notificacion.save()

            cliente_correo = cliente.id_usuario.correo_electronico
            motivo = notificacion.motivo
            notas = notificacion.notas if notificacion.notas else "Sin notas."

            send_mail(
                subject=f"Recordatorio: {motivo}",
                message=f"Hola {cliente.id_usuario.nombres},\n\nEste es un recordatorio:\nMotivo: {motivo}\nNotas: {notas}\n\nAtentamente, Motors Safety Net.",
                from_email='motorssafetynet@gmail.com',
                recipient_list=[cliente_correo],
                fail_silently=False
            )

            messages.success(request, "Notificación registrada correctamente.")
            registro_notificacion = True
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = NotificacionForm()
    return render(request, 'notificaciones.html', {'form': form, 'notificaciones': notificaciones, 'registro_notificacion': registro_notificacion, 'hoy': hoy})


@login_required
def edit_notificacion(request, id_notificacion):
    notificacion = get_object_or_404(Notificaciones, id_notificaciones=id_notificacion)
    act_notificacion = False
    if request.method == "POST":
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            act_notificacion = True
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = NotificacionForm(instance=notificacion)
    return render(request, 'editNotificacion.html', {'form': form, 'notificacion': notificacion, 'act_notificacion': act_notificacion})

@login_required
def eliminar_notificacion(request, id_notificacion):
    notificacion = get_object_or_404(Notificaciones, id_notificaciones=id_notificacion)
    notificacion.delete()
    messages.success(request, "Notificación eliminada correctamente.")
    return redirect('cliente:notificaciones')


def ejecutar_notificaciones(request):
    enviar_notificacion.delay()
    return JsonResponse({"mensaje": "Tarea de notificaciones en ejecución."})