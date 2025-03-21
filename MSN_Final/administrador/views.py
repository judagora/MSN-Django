from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm, CambiarContraseñaForm
from django.core.mail import send_mail
from django.urls import reverse
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.contrib.auth import update_session_auth_hash




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
        id_mecanico = request.POST.get('idMecanico')

        try:
            administrador = Administrador.objects.get(id_administrador=id_administrador)
            mecanico = Mecanico.objects.get(id_mecanico=id_mecanico)

            TallerMecanico.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                horario_de_atencion=horario,
                id_administrador=administrador,
                id_mecanico=mecanico
            )
            return redirect('administrador:talleresMecanico')
        except Exception as e:
            messages.error(request, f'Error al registrar el taller: {str(e)}')

    # Obtener listas de administradores y mecánicos para el formulario
    administradores = Administrador.objects.all()
    mecanicos = Mecanico.objects.all()
    return render(request, 'insertarTaller.html', {
        'administradores': administradores,
        'mecanicos': mecanicos
    })



def modificarMecanico(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    mecanico = get_object_or_404(Mecanico, id_usuario=usuario)

    if request.method == 'POST':
        form = RegistroMecanicoForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            mecanico.horario_de_trabajo = form.cleaned_data['horario_de_trabajo']
            mecanico.experiencia_laboral = form.cleaned_data['experiencia_laboral']
            mecanico.save()
            return redirect('administrador:mecanicos')
           
        else:
            # Imprimir errores en la consola para depuración
            print("Errores del formulario:", form.errors)
    else:
        form = RegistroMecanicoForm(instance=usuario, initial={
            'horario_de_trabajo': mecanico.horario_de_trabajo,
            'experiencia_laboral': mecanico.experiencia_laboral,
        })

    return render(request, 'modificarMecanico.html', {'form': form, 'mecanico': mecanico})



def insertarMecanico(request):
    if request.method == 'POST':
        print("Datos enviados:", request.POST)  # Depuración: Verifica los datos enviados
        form = RegistroMecanicoForm(request.POST)
        if form.is_valid():
            print("El formulario es válido")  # Depuración en consola
            try:
                usuario = form.save(commit=False)
                usuario.rol_usuario = "Mecanico"
                usuario.save()
                print(f"Usuario creado con ID: {usuario.id_usuario}")

                # Verificar si el usuario se guardó correctamente
                if usuario.id_usuario:
                    mecanico = Mecanico.objects.create(
                        id_usuario=usuario,
                        horario_de_trabajo=form.cleaned_data['horario_de_trabajo'],
                        experiencia_laboral=form.cleaned_data['experiencia_laboral']
                    )
                    print(f"Mecánico creado con ID: {mecanico.id_mecanico}")

                    # Enviar correo electrónico al mecánico
                    subject = 'Bienvenido a Motors Safety Net'
                    message = f'''
                        Hola {usuario.nombres},

                        Te has registrado como mecánico en Motors Safety Net. Aquí están tus credenciales:

                        Correo Electrónico: {usuario.correo_electronico}
                        Contraseña: {form.cleaned_data['password1']}

                        Por favor ingresa al siguiente link para modificar tu contraseña:
                        {request.build_absolute_uri(reverse('administrador:cambiar_contraseña'))}

                        Gracias,
                        Equipo de Motors Safety Net
                    '''
                    from_email = 'motorssafetynet@gmail.com'  # Tu dirección de Gmail
                    recipient_list = [usuario.correo_electronico]  # Correo del mecánico

                    # Enviar el correo
                    try:
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                        print("Correo enviado correctamente")
                        messages.success(request, "El mecánico se ha registrado correctamente y se ha enviado un correo.")
                    except Exception as e:
                        print(f"Error al enviar el correo: {str(e)}")
                        messages.error(request, f"Error al enviar el correo: {str(e)}")
                else:
                    messages.error(request, "No se pudo obtener el ID del usuario.")
            except Exception as e:
                messages.error(request, f"Error al registrar el mecánico: {str(e)}")
                print(f"Error al registrar el mecánico: {str(e)}")  # Depuración en consola
        else:
            print("Errores del formulario:", form.errors)  # Imprime los errores del formulario en la consola
            messages.error(request, "Hubo un error en el formulario. Por favor, corrige los errores.")
    else:
        form = RegistroMecanicoForm()

    return render(request, 'insertarMecanico.html', {'form': form})




def cambiar_contraseña(request):
    if request.method == 'POST':
        form = CambiarContraseñaForm(request.user, request.POST)
        if form.is_valid():
            usuario = form.save()  # Cambia la contraseña
            update_session_auth_hash(request, usuario)  # Actualiza la sesión para evitar que el usuario sea desconectado

            # Obtén la nueva contraseña
            nueva_contraseña = form.cleaned_data['new_password1']

            # Enviar correo electrónico con la nueva contraseña
            subject = 'Contraseña actualizada en Motors Safety Net'
            message = f'''
                Hola {usuario.nombres},

                Tu contraseña en Motors Safety Net ha sido actualizada. Aquí está tu nueva contraseña:

                Nueva contraseña: {nueva_contraseña}

                Por seguridad, te recomendamos cambiar esta contraseña después de iniciar sesión.

                Gracias,
                Equipo de Motors Safety Net
            '''
            from_email = 'motorssafetynet@gmail.com'  # Tu dirección de Gmail
            recipient_list = [usuario.email]  # Correo del usuario

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "Tu contraseña ha sido actualizada y se ha enviado un correo con la nueva contraseña.")
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {str(e)}")

            return redirect('inicio')  # Redirige al inicio después de cambiar la contraseña
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CambiarContraseñaForm(request.user)

    return render(request, 'cambiar_contraseña.html', {'form': form})





def eliminar_mecanico(request, id_usuario):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        usuario.delete()
        messages.success(request, 'Mecánico eliminado exitosamente.')
    return redirect('administrador:mecanicos')



def mantenimientos (request):
      mantenimientos = Mantenimiento.objects.all()
      return render(request, 'mantenimientos.html', {'mantenimientos': mantenimientos})

def historialesVehiculo (request):
    # Obtener todos los vehículos
    vehiculos = Vehiculo.objects.all()
    
    # Pasar los datos a la plantilla
    return render(request, 'historialesVehiculo.html', {'vehiculos': vehiculos})

def talleresMecanico (request):
    talleres = TallerMecanico.objects.all()
    return render(request, 'talleresMecanico.html', {'talleres': talleres})

def mecanicos (request):
    # Obtener todos los mecánicos con sus usuarios asociados
    mecanicos = Mecanico.objects.select_related('id_usuario').all()
    
    # Pasar los datos a la plantilla
    return render(request, 'mecanicos.html', {'mecanicos': mecanicos})



def peritajes (request):
    peritajes = Peritaje.objects.all()
    return render(request, 'peritajes.html', {'peritajes': peritajes})



def modificarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)

    if request.method == 'POST':
        peritaje.descripcion = request.POST.get('descripcion')
        peritaje.costo = request.POST.get('costo')
        peritaje.notas_adicionales = request.POST.get('notas_adicionales')
        peritaje.save()

        return redirect('administrador:peritajes')

    return render(request, 'modificarPeritaje.html', {'peritaje': peritaje})



def modificarTaller(request, id_taller_mecanico):
    taller = get_object_or_404(TallerMecanico, id_taller_mecanico=id_taller_mecanico)

    if request.method == 'POST':
        taller.nombre = request.POST.get('nombre')
        taller.direccion = request.POST.get('direccion')
        taller.telefono = request.POST.get('telefono')
        taller.horario_de_atencion = request.POST.get('horario')
        taller.id_administrador = Administrador.objects.get(id_administrador=request.POST.get('idAdministrador'))
        taller.id_mecanico = Mecanico.objects.get(id_mecanico=request.POST.get('idMecanico'))
        taller.save()

        return redirect('administrador:talleresMecanico')


    administradores = Administrador.objects.all()
    mecanicos = Mecanico.objects.all()
    return render(request, 'modificarTaller.html', {
        'taller': taller,
        'administradores': administradores,
        'mecanicos': mecanicos
    })



def eliminarTaller(request, id_taller):
    taller = get_object_or_404(TallerMecanico, id_taller=id_taller)
    taller.delete()
    messages.success(request, 'Taller eliminado exitosamente.')
    return redirect('administrador:talleresMecanico')



def eliminarPeritaje(request, id_peritaje):
    peritaje = get_object_or_404(Peritaje, id_peritaje=id_peritaje)
    peritaje.delete()
    messages.success(request, 'Peritaje eliminado exitosamente.')
    return redirect('administrador:peritajes')


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

def eliminar_mantenimiento(request, id_mantenimiento):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id_mantenimiento)
    mantenimiento.delete()
    messages.success(request, 'Mantenimiento eliminado exitosamente.')
    return redirect('administrador:mantenimientos')
