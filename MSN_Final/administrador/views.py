from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico, MantenimientoProgramado
from .forms import TallerMecanicoForm, ModificarMecanicoForm
from django.conf import settings

@login_required
def inicio(request):
    return render(request, 'indexAdministrador.html')

@login_required
def insertarTaller(request):
    if request.method == 'POST':
        form = TallerMecanicoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'insertarTaller.html', {
                    'form': TallerMecanicoForm(),
                    'administradores': Administrador.objects.all(),
                    'success_message': 'Taller registrado exitosamente'
                })
            except Exception as e:
                error_message = f'Error al registrar el taller: {str(e)}'
        else:
            error_message = "Por favor corrige los errores en el formulario"
    else:
        form = TallerMecanicoForm()
    
    return render(request, 'insertarTaller.html', {
        'form': form,
        'administradores': Administrador.objects.all(),
        'error_message': error_message if 'error_message' in locals() else None,
        'form_errors': form.errors.get_json_data() if 'form' in locals() else None
    })

@login_required
def modificarMecanico(request, id_usuario):
    mecanico = get_object_or_404(Mecanico, id_usuario=id_usuario)
    context = {
        'mecanico': mecanico,
        'talleres': TallerMecanico.objects.all()
    }
    
    if request.method == 'POST':
        # Usa el nuevo formulario de modificación
        form = ModificarMecanicoForm(request.POST, instance=mecanico.id_usuario)
        
        if form.is_valid():
            try:
                # Guarda el usuario sin tocar la contraseña
                usuario = form.save(commit=False)
                usuario.save()  # Guarda sin modificar la contraseña
                
                # Actualiza los campos específicos del mecánico
                mecanico.horario_de_trabajo = form.cleaned_data['horario_de_trabajo']
                mecanico.experiencia_laboral = form.cleaned_data['experiencia_laboral']
                mecanico.id_taller_mecanico = form.cleaned_data['id_taller_mecanico']
                mecanico.save()
                
                context['success_message'] = 'Mecánico actualizado exitosamente'
                return render(request, 'mecanicos.html', {
                    'mecanicos': Mecanico.objects.select_related('id_usuario').all(),
                    'success_message': context['success_message']
                })
            except Exception as e:
                context['error_message'] = f'Error al actualizar el mecánico: {str(e)}'
        else:
            context['error_message'] = "Por favor corrige los errores en el formulario"
            context['form_errors'] = form.errors
    
    # Inicializa el formulario con los datos actuales
    initial_data = {
        'horario_de_trabajo': mecanico.horario_de_trabajo,
        'experiencia_laboral': mecanico.experiencia_laboral,
        'id_taller_mecanico': mecanico.id_taller_mecanico
    }
    context['form'] = ModificarMecanicoForm(instance=mecanico.id_usuario, initial=initial_data)
    
    return render(request, 'modificarMecanico.html', context)


@login_required
def insertarMecanico(request):
    context = {
        'talleres': TallerMecanico.objects.all(),
        'form': RegistroMecanicoForm()
    }

    if request.method == 'POST':
        form = RegistroMecanicoForm(request.POST)
        context['form'] = form
        
        if form.is_valid():
            try:
                # Crear usuario
                usuario = form.save(commit=False)
                usuario.rol_usuario = "Mecanico"
                usuario.save()

                # Asignar taller
                id_taller = request.POST.get('id_taller_mecanico')
                taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller) if id_taller else None

                # Crear mecánico
                Mecanico.objects.create(
                    id_usuario=usuario,
                    horario_de_trabajo=form.cleaned_data['horario_de_trabajo'],
                    experiencia_laboral=form.cleaned_data['experiencia_laboral'],
                    id_taller_mecanico=taller
                )

                # Enviar correo
                subject = 'Registro exitoso en Motors Safety Net'
                message_email = f"""
                Hola {usuario.nombres},

                Tus credenciales:
                Usuario: {usuario.correo_electronico}
                Contraseña: {form.cleaned_data['password1']}
                """
                
                send_mail(
                    subject,
                    message_email,
                    settings.DEFAULT_FROM_EMAIL,
                    [usuario.correo_electronico],
                    fail_silently=False,
                )

                # Mensaje de éxito
                request.session['success_message'] = "Mecánico registrado y correo enviado exitosamente"
                return redirect('administrador:mecanicos')

            except Exception as e:
                context['error_message'] = f"Error al registrar el mecánico: {str(e)}"
        else:
            context['error_message'] = "Por favor corrige los errores en el formulario"
            context['error_details'] = [f"{field}: {error}" for field, errors in form.errors.items() for error in errors]
    
    return render(request, 'insertarMecanico.html', context)


@login_required
def eliminar_mecanico(request, id_usuario):
    context = {}
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            usuario.delete()
            context['success_message'] = 'Mecánico eliminado exitosamente.'
        except Usuario.DoesNotExist:
            context['error_message'] = 'El mecánico no existe'
        except Exception as e:
            context['error_message'] = f'Error al eliminar el mecánico: {str(e)}'
    
    context['mecanicos'] = Mecanico.objects.select_related('id_usuario').all()
    return render(request, 'mecanicos.html', context)


@login_required
def mantenimientos(request):
    mantenimientos_programados = MantenimientoProgramado.objects.select_related(
        'id_mecanico',
        'id_vehiculo',
        'id_taller_mecanico'
    ).all()
    
    return render(request, 'mantenimientos.html', {
        'mantenimientos_programados': mantenimientos_programados
    })


@login_required
def historialesVehiculo(request):
    return render(request, 'historialesVehiculo.html', {
        'vehiculos': Vehiculo.objects.select_related('id_cliente__id_usuario').all()
    })

@login_required
def talleresMecanico(request):
    return render(request, 'talleresMecanico.html', {
        'talleres': TallerMecanico.objects.all()
    })

@login_required
def mecanicos(request):
    context = {
        'mecanicos': Mecanico.objects.select_related('id_usuario').all()
    }
    
      # Manejar mensajes de sesión
    if 'success_message' in request.session:
        context['success_message'] = request.session.pop('success_message')
    if 'error_message' in request.session:
        context['error_message'] = request.session.pop('error_message')
    
    return render(request, 'mecanicos.html', context)

    

@login_required
def peritajes(request):
    return render(request, 'peritajes.html', {
        'peritajes': Peritaje.objects.all()
    })

@login_required
def modificarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)
    context = {}

    if request.method == 'POST':
        try:
            peritaje.descripcion = request.POST.get('descripcion')
            peritaje.costo = request.POST.get('costo')
            peritaje.notas_adicionales = request.POST.get('notas_adicionales')
            peritaje.save()
            context['success_message'] = 'Peritaje actualizado exitosamente'
        except Exception as e:
            context['error_message'] = f'Error al actualizar el peritaje: {str(e)}'
        
        context['peritajes'] = Peritaje.objects.all()
        return render(request, 'peritajes.html', context)

    return render(request, 'modificarPeritaje.html', {
        'peritaje': peritaje
    })

@login_required
def modificarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)
    
    if request.method == 'POST':
        form = TallerMecanicoForm(request.POST, instance=taller)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'modificarTaller.html', {
                    'form': form,
                    'taller': taller,
                    'administradores': Administrador.objects.all(),
                    'success_message': 'Taller actualizado exitosamente'
                })
            except Exception as e:
                error_message = f'Error al actualizar el taller: {str(e)}'
        else:
            error_message = "Por favor corrige los errores en el formulario"
    else:
        form = TallerMecanicoForm(instance=taller)
    
    return render(request, 'modificarTaller.html', {
        'form': form,
        'taller': taller,
        'administradores': Administrador.objects.all(),
        'error_message': error_message if 'error_message' in locals() else None,
        'form_errors': form.errors.get_json_data() if 'form' in locals() and form.errors else None
    })

@login_required
def eliminarTaller(request, id_taller_mecanico):
    context = {}
    try:
        taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller_mecanico)
        
        if taller.mecanico_set.exists():
            context['error_message'] = 'No se puede eliminar el taller porque tiene mecánicos asociados'
        else:
            taller.delete()
            context['success_message'] = 'Taller eliminado exitosamente'
            
    except TallerMecanico.DoesNotExist:
        context['error_message'] = 'El taller no existe'
    except Exception as e:
        context['error_message'] = f'Error al eliminar el taller: {str(e)}'
    
    context['talleres'] = TallerMecanico.objects.all()
    return render(request, 'talleresMecanico.html', context)

@login_required
def eliminarPeritaje(request, id_peritaje):
    context = {}
    try:
        peritaje = Peritaje.objects.get(id_peritaje=id_peritaje)
        peritaje.delete()
        context['success_message'] = 'Peritaje eliminado exitosamente.'
    except Peritaje.DoesNotExist:
        context['error_message'] = 'El peritaje no existe'
    except Exception as e:
        context['error_message'] = f'Error al eliminar el peritaje: {str(e)}'
    
    context['peritajes'] = Peritaje.objects.all()
    return render(request, 'peritajes.html', context)

@login_required
def modificarMantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)
    context = {}

    if request.method == 'POST':
        try:
            mantenimiento.tipo_mantenimiento = request.POST.get('tipoMantenimiento')
            mantenimiento.descripcion = request.POST.get('descripcionMantenimiento')
            mantenimiento.costo = request.POST.get('costoMantenimiento')
            mantenimiento.notas_adicionales = request.POST.get('notasAdicionalesMantenimiento')
            mantenimiento.save()
            context['success_message'] = 'Mantenimiento modificado exitosamente.'
        except Exception as e:
            context['error_message'] = f'Error al modificar el mantenimiento: {str(e)}'
        
        context['mantenimientos'] = Mantenimiento.objects.all()
        return render(request, 'mantenimientos.html', context)

    return render(request, 'modificarMantenimiento.html', {
        'mantenimiento': mantenimiento
    })

@login_required
def eliminar_mantenimiento(request, id_mantenimiento):
    context = {}
    try:
        mantenimiento = Mantenimiento.objects.get(id_mantenimiento=id_mantenimiento)
        mantenimiento.delete()
        context['success_message'] = 'Mantenimiento eliminado exitosamente.'
    except Mantenimiento.DoesNotExist:
        context['error_message'] = 'El mantenimiento no existe'
    except Exception as e:
        context['error_message'] = f'Error al eliminar el mantenimiento: {str(e)}'
    
    context['mantenimientos'] = Mantenimiento.objects.all()
    return render(request, 'mantenimientos.html', context)