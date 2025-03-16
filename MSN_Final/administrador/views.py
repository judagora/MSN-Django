from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistroMecanicoForm
from inicio.models import Mecanico, Usuario
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.contrib.auth.hashers import make_password  # Para hashear la contraseña manualmente


# Create your views here.
def inicio (request):
    return render(request, 'indexAdministrador.html')

def insertarTaller (request):
    return render(request, 'insertarTaller.html')

def insertarMantenimiento (request):
    return render(request, 'insertarMantenimiento.html')



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
            messages.error(request, "El formulario no es válido. Corrige los errores.")
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
    return render(request, 'mantenimientos.html')

def historialesVehiculo (request):
    return render(request, 'historialesVehiculo.html')

def talleresMecanico (request):
    return render(request, 'talleresMecanico.html')

def mecanicos (request):
    # Obtener todos los mecánicos con sus usuarios asociados
    mecanicos = Mecanico.objects.select_related('id_usuario').all()
    
    # Pasar los datos a la plantilla
    return render(request, 'mecanicos.html', {'mecanicos': mecanicos})

def peritajes (request):
    return render(request, 'peritajes.html')

def modificarPeritaje (request):
    return render(request, 'modificarPeritaje.html')

def modificarTaller (request):
    return render(request, 'modificarTaller.html')

def modificarMantenimiento (request):
    return render(request, 'modificarMantenimiento.html')
