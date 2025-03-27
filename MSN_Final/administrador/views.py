from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.contrib.auth import update_session_auth_hash



@login_required
# Create your views here.
def inicio (request):
    return render(request, 'indexAdministrador.html')

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
            return redirect('administrador:talleresMecanico')
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
                # Actualizar usuario
                usuario = form.save()
                
                # Actualizar datos específicos del mecánico
                mecanico.horario_de_trabajo = request.POST.get('horario_de_trabajo')
                mecanico.experiencia_laboral = request.POST.get('experiencia_laboral')
                
                # Actualizar taller si se cambió
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
        print("Datos enviados:", request.POST)
        form = RegistroMecanicoForm(request.POST)
        
        if form.is_valid():
            print("El formulario es válido")
            try:
                # Crear usuario
                usuario = form.save(commit=False)
                usuario.rol_usuario = "Mecanico"
                usuario.save()
                print(f"Usuario creado con ID: {usuario.id_usuario}")

                # Obtener el taller seleccionado
                id_taller = request.POST.get('id_taller_mecanico')
                taller = TallerMecanico.objects.get(id_taller_mecanico=id_taller) if id_taller else None

                # Crear mecánico
                mecanico = Mecanico.objects.create(
                    id_usuario=usuario,
                    horario_de_trabajo=form.cleaned_data['horario_de_trabajo'],
                    experiencia_laboral=form.cleaned_data['experiencia_laboral'],
                    id_taller_mecanico=taller
                )
                print(f"Mecánico creado con ID: {mecanico.id_mecanico}")

                # Enviar correo electrónico
                subject = 'Bienvenido a Motors Safety Net'
                message = f'''
                    Hola {usuario.nombres},

                    Te has registrado como mecánico en Motors Safety Net. Aquí están tus credenciales:

                    Correo Electrónico: {usuario.correo_electronico}
                    Contraseña: {form.cleaned_data['password1']}


                    Gracias,
                    Equipo de Motors Safety Net
                '''
                from_email = 'motorssafetynet@gmail.com'
                recipient_list = [usuario.correo_electronico]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print("Correo enviado correctamente")
                    messages.success(request, "Mecánico registrado y correo enviado exitosamente")
                except Exception as e:
                    print(f"Error al enviar el correo: {str(e)}")
                    messages.warning(request, f"Mecánico registrado pero error al enviar correo: {str(e)}")

                return redirect('administrador:mecanicos')

            except Exception as e:
                messages.error(request, f"Error al registrar el mecánico: {str(e)}")
                print(f"Error al registrar el mecánico: {str(e)}")
        else:
            print("Errores del formulario:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroMecanicoForm()

    # Obtener todos los talleres para el select
    talleres = TallerMecanico.objects.all()
    return render(request, 'insertarMecanico.html', {
        'form': form,
        'talleres': talleres
    })


@login_required
def eliminar_mecanico(request, id_usuario):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        usuario.delete()
        messages.success(request, 'Mecánico eliminado exitosamente.')
    return redirect('administrador:mecanicos')


@login_required
def mantenimientos (request):
      mantenimientos = Mantenimiento.objects.all()
      return render(request, 'mantenimientos.html', {'mantenimientos': mantenimientos})

@login_required
def historialesVehiculo(request):
    # Obtener todos los vehículos con la información del cliente y el usuario
    vehiculos = Vehiculo.objects.select_related('id_cliente__id_usuario').all()
    return render(request, 'historialesVehiculo.html', {'vehiculos': vehiculos})
    
    # Pasar los datos a la plantilla
    return render(request, 'historialesVehiculo.html', {'vehiculos': vehiculos})

@login_required
def talleresMecanico (request):
    talleres = TallerMecanico.objects.all()
    return render(request, 'talleresMecanico.html', {'talleres': talleres})

@login_required
def mecanicos (request):
    # Obtener todos los mecánicos con sus usuarios asociados
    mecanicos = Mecanico.objects.select_related('id_usuario').all()
    
    # Pasar los datos a la plantilla
    return render(request, 'mecanicos.html', {'mecanicos': mecanicos})



@login_required
def peritajes (request):
    peritajes = Peritaje.objects.all()
    return render(request, 'peritajes.html', {'peritajes': peritajes})



@login_required
def modificarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)

    if request.method == 'POST':
        peritaje.descripcion = request.POST.get('descripcion')
        peritaje.costo = request.POST.get('costo')
        peritaje.notas_adicionales = request.POST.get('notas_adicionales')
        peritaje.save()

        return redirect('administrador:peritajes')

    return render(request, 'modificarPeritaje.html', {'peritaje': peritaje})



@login_required
def modificarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)
    administradores = Administrador.objects.all()  # Obtener todos los administradores

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        horario = request.POST.get('horario')

        try:
            taller.nombre = nombre
            taller.direccion = direccion
            taller.telefono = telefono
            taller.horario_de_atencion = horario
            taller.save()
            messages.success(request, 'Taller actualizado exitosamente')
            return redirect('administrador:talleresMecanico')
        except Exception as e:
            messages.error(request, f'Error al actualizar el taller: {str(e)}')

    return render(request, 'modificarTaller.html', {
        'taller': taller,
        'administradores': administradores  # Pasar los administradores al template
    })



@login_required
def eliminarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)
    
    try:
        # Verificar si el taller tiene mecánicos asociados
        if taller.mecanico_set.exists():
            messages.error(request, 'No se puede eliminar el taller porque tiene mecánicos asociados')
        else:
            taller.delete()
            messages.success(request, 'Taller eliminado exitosamente')
    except Exception as e:
        messages.error(request, f'Error al eliminar el taller: {str(e)}')
    
    return redirect('administrador:talleresMecanico')



@login_required
def eliminarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)
    peritaje.delete()
    messages.success(request, 'Peritaje eliminado exitosamente.')
    return redirect('administrador:peritajes')


@login_required
def modificarMantenimiento (request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)

    if request.method == 'POST':
        mantenimiento.tipo_mantenimiento = request.POST.get('tipoMantenimiento')
        mantenimiento.descripcion = request.POST.get('descripcionMantenimiento')
        mantenimiento.costo = request.POST.get('costoMantenimiento')
        mantenimiento.notas_adicionales = request.POST.get('notasAdicionalesMantenimiento')
        mantenimiento.save()

        messages.success(request, 'Mantenimiento modificado exitosamente.')
        return redirect('administrador:mantenimientos')

    return render(request, 'modificarMantenimiento.html', {'mantenimiento': mantenimiento})

@login_required
def eliminar_mantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)
    mantenimiento.delete()
    messages.success(request, 'Mantenimiento eliminado exitosamente.')
    return redirect('administrador:mantenimientos')
