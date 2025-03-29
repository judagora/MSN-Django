from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico

@login_required
def inicio(request):
    return render(request, 'indexAdministrador.html', {
        'show_message': False
    })

@login_required
def insertarTaller(request):
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        horario = request.POST.get('horario')
        id_administrador = request.POST.get('idAdministrador')

        try:
            administrador = Administrador.objects.get(id_administrador=id_administrador)
            TallerMecanico.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                horario_de_atencion=horario,
                id_administrador=administrador
            )
            message = 'Taller registrado exitosamente'
            message_type = 'success'
            show_message = True
            return redirect('administrador:insertarTaller')
        except Administrador.DoesNotExist:
            message = 'El administrador seleccionado no existe'
            message_type = 'error'
            show_message = True
        except Exception as e:
            message = f'Error al registrar el taller: {str(e)}'
            message_type = 'error'
            show_message = True

    administradores = Administrador.objects.all()
    return render(request, 'insertarTaller.html', {
        'administradores': administradores,
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def modificarMecanico(request, id_usuario):
    mecanico = get_object_or_404(Mecanico, id_usuario=id_usuario)
    message = None
    message_type = None
    show_message = False
    
    if request.method == 'POST':
        form = RegistroMecanicoForm(request.POST, instance=mecanico.id_usuario)
        
        if form.is_valid():
            try:
                usuario = form.save()
                mecanico.horario_de_trabajo = request.POST.get('horario_de_trabajo')
                mecanico.experiencia_laboral = request.POST.get('experiencia_laboral')
                
                id_taller = request.POST.get('id_taller_mecanico')
                if id_taller:
                    mecanico.id_taller_mecanico = TallerMecanico.objects.get(id_taller_mecanico=id_taller)
                else:
                    mecanico.id_taller_mecanico = None
                
                mecanico.save()
                message = 'Mecánico actualizado exitosamente'
                message_type = 'success'
                show_message = True
                return redirect('administrador:mecanicos')
            except Exception as e:
                message = f'Error al actualizar el mecánico: {str(e)}'
                message_type = 'error'
                show_message = True
        else:
            message = "Por favor corrige los errores en el formulario"
            message_type = 'error'
            show_message = True
    else:
        form = RegistroMecanicoForm(instance=mecanico.id_usuario)

    talleres = TallerMecanico.objects.all()
    return render(request, 'modificarMecanico.html', {
        'form': form,
        'mecanico': mecanico,
        'talleres': talleres,
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def insertarMecanico(request):
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        form = RegistroMecanicoForm(request.POST)
        
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                usuario.rol_usuario = "Mecanico"
                usuario.save()

                id_taller = request.POST.get('id_taller_mecanico')
                taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller) if id_taller else None

                Mecanico.objects.create(
                    id_usuario=usuario,
                    horario_de_trabajo=form.cleaned_data['horario_de_trabajo'],
                    experiencia_laboral=form.cleaned_data['experiencia_laboral'],
                    id_taller_mecanico=taller
                )

                subject = '🚀 Bienvenido a Motors Safety Net - Registro Exitoso 🚀'
                message = f"""
                ============================================
                ⚙️ REGISTRO DE MECÁNICO EXITOSO ⚙️
                ============================================

                ¡Bienvenido/a {usuario.nombres}!

                Tus credenciales para acceder al sistema son:

                📌 DATOS DE ACCESO:
                ----------------------------------
                • Correo: {usuario.correo_electronico}
                • Contraseña: {form.cleaned_data['password1']}
                ----------------------------------

                📅 HORARIO ASIGNADO: 
                {form.cleaned_data['horario_de_trabajo']}

                🏢 TALLER: 
                {taller.nombre if taller else "Por asignar"}

                🔧 INFORMACIÓN ADICIONAL:
                ----------------------------------
                • Experiencia: {form.cleaned_data['experiencia_laboral']}
                • Fecha de registro: {usuario.fecha_registro.strftime('%d/%m/%Y')}
                ----------------------------------

                📬 CONTACTO DE SOPORTE:
                ----------------------------------
                ✉️ Email: motorssafetynet@gmail.com
                📞 Teléfono: +1 (234) 567-8901
                ----------------------------------

                ============================================
                ¡Gracias por unirte a nuestra red de profesionales!
                - El equipo de Motors Safety Net -
                ============================================

                ℹ️ Este es un mensaje automático, por favor no responder.
                """
                
                send_mail(
                    subject, 
                    message, 
                    'motorssafetynet@gmail.com', 
                    [usuario.correo_electronico],
                    fail_silently=False
                )
                
                message = "Mecánico registrado y correo enviado exitosamente"
                message_type = "success"
                show_message = True
                return redirect('administrador:mecanicos')

            except Exception as e:
                message = f"Error al registrar el mecánico: {str(e)}"
                message_type = "error"
                show_message = True
        else:
            message = "Por favor corrige los errores en el formulario"
            message_type = "error"
            show_message = True
    else:
        form = RegistroMecanicoForm()

    talleres = TallerMecanico.objects.all()
    return render(request, 'insertarMecanico.html', {
        'form': form,
        'talleres': talleres,
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def eliminar_mecanico(request, id_usuario):
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            usuario.delete()
            message = 'Mecánico eliminado exitosamente.'
            message_type = 'success'
            show_message = True
        except Usuario.DoesNotExist:
            message = 'El mecánico no existe'
            message_type = 'error'
            show_message = True
        except Exception as e:
            message = f'Error al eliminar el mecánico: {str(e)}'
            message_type = 'error'
            show_message = True
            
    return render(request, 'mecanicos.html', {
        'mecanicos': Mecanico.objects.select_related('id_usuario').all(),
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def mantenimientos(request):
    return render(request, 'mantenimientos.html', {
        'mantenimientos': Mantenimiento.objects.all(),
        'show_message': False
    })

@login_required
def historialesVehiculo(request):
    return render(request, 'historialesVehiculo.html', {
        'vehiculos': Vehiculo.objects.select_related('id_cliente__id_usuario').all(),
        'show_message': False
    })

@login_required
def talleresMecanico(request):
    return render(request, 'talleresMecanico.html', {
        'talleres': TallerMecanico.objects.all(),
        'show_message': False
    })

@login_required
def mecanicos(request):
    return render(request, 'mecanicos.html', {
        'mecanicos': Mecanico.objects.select_related('id_usuario').all(),
        'show_message': False
    })

@login_required
def peritajes(request):
    return render(request, 'peritajes.html', {
        'peritajes': Peritaje.objects.all(),
        'show_message': False
    })

@login_required
def modificarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        try:
            peritaje.descripcion = request.POST.get('descripcion')
            peritaje.costo = request.POST.get('costo')
            peritaje.notas_adicionales = request.POST.get('notas_adicionales')
            peritaje.save()
            message = 'Peritaje actualizado exitosamente'
            message_type = 'success'
            show_message = True
        except Exception as e:
            message = f'Error al actualizar el peritaje: {str(e)}'
            message_type = 'error'
            show_message = True
        
        return render(request, 'peritajes.html', {
            'peritajes': Peritaje.objects.all(),
            'message': message,
            'message_type': message_type,
            'show_message': show_message
        })

    return render(request, 'modificarPeritaje.html', {
        'peritaje': peritaje,
        'show_message': False
    })

@login_required
def modificarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)
    administradores = Administrador.objects.all()
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        try:
            taller.nombre = request.POST.get('nombre')
            taller.direccion = request.POST.get('direccion')
            taller.telefono = request.POST.get('telefono')
            taller.horario_de_atencion = request.POST.get('horario')
            taller.save()
            message = 'Taller actualizado exitosamente'
            message_type = 'success'
            show_message = True
            return render(request, 'talleresMecanico.html', {
                'talleres': TallerMecanico.objects.all(),
                'message': message,
                'message_type': message_type,
                'show_message': show_message
            })
        except Exception as e:
            message = f'Error al actualizar el taller: {str(e)}'
            message_type = 'error'
            show_message = True

    return render(request, 'modificarTaller.html', {
        'taller': taller,
        'administradores': administradores,
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def eliminarTaller(request, id_taller_mecanico):
    message = None
    message_type = None
    show_message = False
    
    try:
        taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller_mecanico)
        
        if taller.mecanico_set.exists():
            message = 'No se puede eliminar el taller porque tiene mecánicos asociados'
            message_type = 'error'
            show_message = True
        else:
            taller.delete()
            message = 'Taller eliminado exitosamente'
            message_type = 'success'
            show_message = True
            
    except TallerMecanico.DoesNotExist:
        message = 'El taller no existe'
        message_type = 'error'
        show_message = True
    except Exception as e:
        message = f'Error al eliminar el taller: {str(e)}'
        message_type = 'error'
        show_message = True
    
    return render(request, 'talleresMecanico.html', {
        'talleres': TallerMecanico.objects.all(),
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def eliminarPeritaje(request, id_peritaje):
    message = None
    message_type = None
    show_message = False
    
    try:
        peritaje = Peritaje.objects.get(id_peritaje=id_peritaje)
        peritaje.delete()
        message = 'Peritaje eliminado exitosamente.'
        message_type = 'success'
        show_message = True
    except Peritaje.DoesNotExist:
        message = 'El peritaje no existe'
        message_type = 'error'
        show_message = True
    except Exception as e:
        message = f'Error al eliminar el peritaje: {str(e)}'
        message_type = 'error'
        show_message = True
        
    return render(request, 'peritajes.html', {
        'peritajes': Peritaje.objects.all(),
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })

@login_required
def modificarMantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)
    message = None
    message_type = None
    show_message = False

    if request.method == 'POST':
        try:
            mantenimiento.tipo_mantenimiento = request.POST.get('tipoMantenimiento')
            mantenimiento.descripcion = request.POST.get('descripcionMantenimiento')
            mantenimiento.costo = request.POST.get('costoMantenimiento')
            mantenimiento.notas_adicionales = request.POST.get('notasAdicionalesMantenimiento')
            mantenimiento.save()
            message = 'Mantenimiento modificado exitosamente.'
            message_type = 'success'
            show_message = True
        except Exception as e:
            message = f'Error al modificar el mantenimiento: {str(e)}'
            message_type = 'error'
            show_message = True
            
        return render(request, 'mantenimientos.html', {
            'mantenimientos': Mantenimiento.objects.all(),
            'message': message,
            'message_type': message_type,
            'show_message': show_message
        })

    return render(request, 'modificarMantenimiento.html', {
        'mantenimiento': mantenimiento,
        'show_message': False
    })

@login_required
def eliminar_mantenimiento(request, id_mantenimiento):
    message = None
    message_type = None
    show_message = False
    
    try:
        mantenimiento = Mantenimiento.objects.get(id_mantenimiento=id_mantenimiento)
        mantenimiento.delete()
        message = 'Mantenimiento eliminado exitosamente.'
        message_type = 'success'
        show_message = True
    except Mantenimiento.DoesNotExist:
        message = 'El mantenimiento no existe'
        message_type = 'error'
        show_message = True
    except Exception as e:
        message = f'Error al eliminar el mantenimiento: {str(e)}'
        message_type = 'error'
        show_message = True
        
    return render(request, 'mantenimientos.html', {
        'mantenimientos': Mantenimiento.objects.all(),
        'message': message,
        'message_type': message_type,
        'show_message': show_message
    })