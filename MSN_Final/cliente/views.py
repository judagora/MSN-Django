from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from inicio.models import Cliente
from inicio.models import Vehiculo, Soat, Notificaciones, Mecanico, TallerMecanico, MantenimientoProgramado, VehiculoMantenimiento, VehiculoPeritaje, VehiculoRepuestosModificados
from django.contrib.auth import logout
from .forms import VehiculoForm, ClienteForm, SoatForm, NotificacionForm, MantenimientoForm
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now, localtime, make_aware
from django.core.mail import send_mail, EmailMultiAlternatives
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
            registro_soat = True
        else:
            print(form.errors)
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
            print(form.errors)
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


@login_required
def mantenimiento(request):
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario=usuario).select_related("id_usuario").first()
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)
    manteniminetosCliente = MantenimientoProgramado.objects.filter(id_vehiculo__in=vehiculos).select_related('id_vehiculo', 'id_taller_mecanico', 'id_mecanico')
    tallerMecanico = TallerMecanico.objects.all()
    mantenimiento_valido = False

    if request.method == "POST":
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.save()

            #  **Obteniendo datos**
            taller = mantenimiento.id_taller_mecanico
            mecanico = mantenimiento.id_mecanico
            vehiculo = mantenimiento.id_vehiculo

            #  **Datos del mecánico**
            mecanico_usuario = mecanico.id_usuario
            mecanico_nombre = mecanico_usuario.nombres
            mecanico_correo = mecanico_usuario.correo_electronico

            #  **Datos del cliente**
            cliente_nombre = cliente.id_usuario.nombres
            cliente_correo = cliente.id_usuario.correo_electronico
            cliente_telefono = cliente.id_usuario.telefono

            fecha_formateada = mantenimiento.fecha_mantenimiento.strftime('%d/%m/%Y')  # Ejemplo: 26/03/2025
            hora_mantenimiento = datetime.combine(datetime.today(), mantenimiento.hora_mantenimiento)
            hora_mantenimiento = make_aware(hora_mantenimiento)
            hora_formateada = hora_mantenimiento.strftime('%I:%M %p')

            # **Correo del Cliente**
            asunto_cliente = "📅 Confirmación de Mantenimiento Programado"
            mensaje_cliente = f"""
                <html>
                <body>
                    <h2>¡Mantenimiento Registrado con Éxito! 🔧</h2>
                    <p><b>Estimado {cliente_nombre},</b></p>
                    <p>Tu mantenimiento ha sido programado correctamente. Aquí están los detalles:</p>
                    <ul>
                        <li><b>Taller:</b> {taller.nombre}</li>
                        <li><b>Dirección:</b> {taller.direccion}</li>
                        <li><b>Mecánico:</b> {mecanico_nombre}</li>
                        <li><b>Vehículo:</b> {vehiculo.marca} - {vehiculo.modelo}</li>
                        <li><b>Fecha:</b> { fecha_formateada }</li>
                        <li><b>Hora:</b> { hora_formateada }</li>
                    </ul>
                    <p>Gracias por confiar en nosotros. ¡Nos vemos pronto!</p>
                    <hr>
                    <p><i>Este es un mensaje automático. Por favor, no respondas a este correo.</i></p>
                </body>
                </html>
            """
            email_cliente = EmailMultiAlternatives(asunto_cliente, mensaje_cliente, 'motorssafetynet@gmail.com', [cliente_correo])
            email_cliente.attach_alternative(mensaje_cliente, "text/html")
            email_cliente.send()

            #**Correo del Mecánico**
            asunto_mecanico = "🔧 Nuevo Mantenimiento Asignado"
            mensaje_mecanico = f"""
                <html>
                <body>
                    <h2>¡Tienes un Nuevo Mantenimiento Asignado! 📅</h2>
                    <p><b>Hola {mecanico_nombre},</b></p>
                    <p>Se te ha asignado un nuevo mantenimiento:</p>
                    <ul>
                        <li><b>Cliente:</b> {cliente_nombre}</li>
                        <li><b>Teléfono:</b> {cliente_telefono}</li>
                        <li><b>Vehículo:</b> {vehiculo.marca} - {vehiculo.modelo} (Placa: {vehiculo.placa})</li>
                        <li><b>Tipo de Mantenimiento:</b> {mantenimiento.tipo_Mantenimiento}</li>
                        <li><b>Fecha:</b> { fecha_formateada }</li>
                        <li><b>Hora:</b> { hora_formateada }</li>
                    </ul>
                    <p>¡Prepárate para la cita y brinda el mejor servicio!</p>
                    <hr>
                    <p><i>Este es un mensaje automático. No respondas a este correo.</i></p>
                </body>
                </html>
            """
            email_mecanico = EmailMultiAlternatives(asunto_mecanico, mensaje_mecanico, 'motorssafetynet@gmail.com', [mecanico_correo])
            email_mecanico.attach_alternative(mensaje_mecanico, "text/html")
            email_mecanico.send()

            mantenimiento_valido = True

        else:
           print(form.errors)

    else:
        form = MantenimientoForm()

    return render(request, 'mantenimiento.html', {
        'vehiculos': vehiculos,
        'tallerMecanico': tallerMecanico,
        'mantenimiento_valido': mantenimiento_valido,
        'manteniminetosCliente': manteniminetosCliente,
        'form': form
    })

@login_required
def editar_mantenimiento(request, id_mantenimiento):
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first()
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)
    tallerMecanico = TallerMecanico.objects.all()
    mantenimiento = get_object_or_404(MantenimientoProgramado, id_mantenimiento=id_mantenimiento)
    mantenimiento_valido = False
    if request.method == "POST":
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            mantenimiento_valido = True
        else:
            print(form.errors)
    else:
        form = MantenimientoForm(instance=mantenimiento)
    return render(request, 'editMantenimiento.html', {'form': form, 'mantenimiento': mantenimiento, 'mantenimiento_valido': mantenimiento_valido, 'vehiculos': vehiculos, 'tallerMecanico': tallerMecanico})

@login_required
def eliminar_mantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(MantenimientoProgramado, id_mantenimiento=id_mantenimiento)
    mantenimiento.delete()
    messages.success(request, "Mantenimiento eliminado correctamente.")
    return redirect('cliente:mantenimiento')

def obtener_mecanicos(request):
    taller_id = request.GET.get('taller_id')

    if not taller_id:
        return JsonResponse({'error': 'No se proporcionó el ID del taller'}, status=400)

    # Filtrar mecánicos por taller mecánico
    mecanicos = Mecanico.objects.filter(id_taller_mecanico_id=taller_id).select_related('id_usuario').values('id_mecanico', 'id_usuario__nombres')

    return JsonResponse(list(mecanicos), safe=False)


@login_required
def procedimientos(request):
    usuario = request.user
    cliente = Cliente.objects.filter(id_usuario = usuario).first()
    vehiculos = Vehiculo.objects.filter(id_cliente=cliente)
    mantenimientos = VehiculoMantenimiento.objects.filter(id_vehiculo__in=vehiculos).select_related('id_mantenimiento')
    peritajes = VehiculoPeritaje.objects.filter(id_vehiculo__in=vehiculos).select_related('id_peritaje')
    repuestos = VehiculoRepuestosModificados.objects.filter(id_vehiculo__in=vehiculos).select_related('id_repuestos_modificados')

    procedimientos = []

    for mantenimiento in mantenimientos:
        procedimientos.append({
            'tipo': f"Mantenimiento {mantenimiento.id_mantenimiento.tipo_mantenimiento}",
            'vehiculo': f"{mantenimiento.id_vehiculo.marca} {mantenimiento.id_vehiculo.modelo} ({mantenimiento.id_vehiculo.placa})",
            'mecanico': mantenimiento.id_mantenimiento.mecanicomantenimiento_set.first().id_mecanico.id_usuario.nombres,
            'notas': mantenimiento.id_mantenimiento.notas_adicionales or "Sin notas"
        })

    for peritaje in peritajes:
        procedimientos.append({
            'tipo': "Peritaje",
            'vehiculo': f"{peritaje.id_vehiculo.marca} {peritaje.id_vehiculo.modelo} ({peritaje.id_vehiculo.placa})",
            'mecanico': peritaje.id_peritaje.mecanicoperitaje_set.first().id_mecanico.id_usuario.nombres,
            'notas': peritaje.id_peritaje.notas_adicionales or "Sin notas"
        })

    for repuesto in repuestos:
        procedimientos.append({
            'tipo': "Cambio de Repuestos",
            'vehiculo': f"{repuesto.id_vehiculo.marca} {repuesto.id_vehiculo.modelo} ({repuesto.id_vehiculo.placa})",
            'mecanico': repuesto.id_repuestos_modificados.mecanicorepuestosmodificados_set.first().id_mecanico.id_usuario.nombres,
            'notas': "Reemplazo de pieza: " + repuesto.id_repuestos_modificados.descripcion
        })
    
    context = {
        'procedimientos': procedimientos,
    }

    return render(request, 'modificaciones.html', context)