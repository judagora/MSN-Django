from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from inicio.models import Mecanico, Usuario, Vehiculo, Mantenimiento, Peritaje, Administrador, TallerMecanico
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.contrib.auth.hashers import make_password  # Para hashear la contraseña manualmente


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
            messages.success(request, 'Taller registrado exitosamente.')
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
            messages.success(request, 'Mecánico modificado exitosamente.')            
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

                # Verificar si usuario se guardó correctamente
                if usuario.id_usuario:
                    mecanico = Mecanico.objects.create(
                        id_usuario=usuario,
                        horario_de_trabajo=form.cleaned_data['horario_de_trabajo'],
                        experiencia_laboral=form.cleaned_data['experiencia_laboral']
                    )
                    print(f"Mecánico creado con ID: {mecanico.id_mecanico}")

                    messages.success(request, "El mecánico se ha registrado correctamente.")
                else:
                    messages.error(request, "No se pudo obtener el ID del usuario.")
            except Exception as e:
                messages.error(request, f"Error al registrar el mecánico: {str(e)}")
                print(f"Error al registrar el mecánico: {str(e)}")  # Depuración en consola
        else:
            print("Errores del formulario:", form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = RegistroMecanicoForm()

    return render(request, 'insertarMecanico.html', {'form': form})



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

        messages.success(request, 'Peritaje modificado exitosamente.')

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

        messages.success(request, 'Taller modificado exitosamente.')

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
