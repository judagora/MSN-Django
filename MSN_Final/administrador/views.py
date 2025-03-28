from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def inicio(request):
    return render(request, 'indexAdministrador.html')

@login_required
def insertarTaller(request):
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
            messages.success(request, 'Taller registrado exitosamente')
            return redirect('administrador:insertarTaller')
        except Administrador.DoesNotExist:
            messages.error(request, 'El administrador seleccionado no existe')
        except Exception as e:
            messages.error(request, f'Error al registrar el taller: {str(e)}')

    administradores = Administrador.objects.all()
    return render(request, 'insertarTaller.html', {
        'administradores': administradores
    })

@login_required
def modificarMecanico(request, id_usuario):
    mecanico = get_object_or_404(Mecanico, id_usuario=id_usuario)
    
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
                messages.success(request, 'Mecánico actualizado exitosamente')
                return redirect('administrador:mecanicos')
            except Exception as e:
                messages.error(request, f'Error al actualizar el mecánico: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroMecanicoForm(instance=mecanico.id_usuario)

    talleres = TallerMecanico.objects.all()
    return render(request, 'modificarMecanico.html', {
        'form': form,
        'mecanico': mecanico,
        'talleres': talleres
    })

@login_required
def insertarMecanico(request):
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
                
                messages.success(request, "Mecánico registrado y correo enviado exitosamente")
                return redirect('administrador:mecanicos')

            except Exception as e:
                messages.error(request, f"Error al registrar el mecánico: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroMecanicoForm()

    talleres = TallerMecanico.objects.all()
    return render(request, 'insertarMecanico.html', {
        'form': form,
        'talleres': talleres
    })

@login_required
def eliminar_mecanico(request, id_usuario):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            usuario.delete()
            messages.success(request, 'Mecánico eliminado exitosamente.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El mecánico no existe')
        except Exception as e:
            messages.error(request, f'Error al eliminar el mecánico: {str(e)}')
            
    return redirect('administrador:mecanicos')

@login_required
def mantenimientos(request):
    mantenimientos = Mantenimiento.objects.all()
    return render(request, 'mantenimientos.html', {'mantenimientos': mantenimientos})

@login_required
def historialesVehiculo(request):
    vehiculos = Vehiculo.objects.select_related('id_cliente__id_usuario').all()
    return render(request, 'historialesVehiculo.html', {'vehiculos': vehiculos})

@login_required
def talleresMecanico(request):
    talleres = TallerMecanico.objects.all()
    return render(request, 'talleresMecanico.html', {'talleres': talleres})

@login_required
def mecanicos(request):
    mecanicos = Mecanico.objects.select_related('id_usuario').all()
    return render(request, 'mecanicos.html', {'mecanicos': mecanicos})

@login_required
def peritajes(request):
    peritajes = Peritaje.objects.all()
    return render(request, 'peritajes.html', {'peritajes': peritajes})

@login_required
def modificarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)

    if request.method == 'POST':
        try:
            peritaje.descripcion = request.POST.get('descripcion')
            peritaje.costo = request.POST.get('costo')
            peritaje.notas_adicionales = request.POST.get('notas_adicionales')
            peritaje.save()
            messages.success(request, 'Peritaje actualizado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar el peritaje: {str(e)}')
        
        return redirect('administrador:peritajes')

    return render(request, 'modificarPeritaje.html', {'peritaje': peritaje})

@login_required
def modificarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)
    administradores = Administrador.objects.all()

    if request.method == 'POST':
        try:
            taller.nombre = request.POST.get('nombre')
            taller.direccion = request.POST.get('direccion')
            taller.telefono = request.POST.get('telefono')
            taller.horario_de_atencion = request.POST.get('horario')
            taller.save()
            messages.success(request, 'Taller actualizado exitosamente')
            return redirect('administrador:talleresMecanico')
        except Exception as e:
            messages.error(request, f'Error al actualizar el taller: {str(e)}')

    return render(request, 'modificarTaller.html', {
        'taller': taller,
        'administradores': administradores
    })

@login_required
def eliminarTaller(request, id_taller_mecanico):
    try:
        taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller_mecanico)
        
        if taller.mecanico_set.exists():
            messages.error(request, 'No se puede eliminar el taller porque tiene mecánicos asociados')
        else:
            taller.delete()
            messages.success(request, 'Taller eliminado exitosamente')
            
    except TallerMecanico.DoesNotExist:
        messages.error(request, 'El taller no existe')
    except Exception as e:
        messages.error(request, f'Error al eliminar el taller: {str(e)}')
    
    return redirect('administrador:talleresMecanico')

@login_required
def eliminarPeritaje(request, id_peritaje):
    try:
        peritaje = Peritaje.objects.get(id_peritaje=id_peritaje)
        peritaje.delete()
        messages.success(request, 'Peritaje eliminado exitosamente.')
    except Peritaje.DoesNotExist:
        messages.error(request, 'El peritaje no existe')
    except Exception as e:
        messages.error(request, f'Error al eliminar el peritaje: {str(e)}')
        
    return redirect('administrador:peritajes')

@login_required
def modificarMantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)

    if request.method == 'POST':
        try:
            mantenimiento.tipo_mantenimiento = request.POST.get('tipoMantenimiento')
            mantenimiento.descripcion = request.POST.get('descripcionMantenimiento')
            mantenimiento.costo = request.POST.get('costoMantenimiento')
            mantenimiento.notas_adicionales = request.POST.get('notasAdicionalesMantenimiento')
            mantenimiento.save()
            messages.success(request, 'Mantenimiento modificado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al modificar el mantenimiento: {str(e)}')
            
        return redirect('administrador:mantenimientos')

    return render(request, 'modificarMantenimiento.html', {'mantenimiento': mantenimiento})

@login_required
def eliminar_mantenimiento(request, id_mantenimiento):
    try:
        mantenimiento = Mantenimiento.objects.get(id_mantenimiento=id_mantenimiento)
        mantenimiento.delete()
        messages.success(request, 'Mantenimiento eliminado exitosamente.')
    except Mantenimiento.DoesNotExist:
        messages.error(request, 'El mantenimiento no existe')
    except Exception as e:
        messages.error(request, f'Error al eliminar el mantenimiento: {str(e)}')
        
    return redirect('administrador:mantenimientos')