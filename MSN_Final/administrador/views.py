from django.shortcuts import render

# Create your views here.
def inicio (request):
    return render(request, 'indexAdministrador.html')

def insertarTaller (request):
    return render(request, 'insertarTaller.html')

def insertarMantenimiento (request):
    return render(request, 'insertarMantenimiento.html')

def modificarMecanico (request):
    return render(request, 'modificarMecanico.html')

def insertarMecanico (request):
    return render(request, 'insertarMecanico.html')

def mantenimientos (request):
    return render(request, 'mantenimientos.html')

def historialesVehiculo (request):
    return render(request, 'historialesVehiculo.html')

def talleresMecanico (request):
    return render(request, 'talleresMecanico.html')

def mecanicos (request):
    return render(request, 'mecanicos.html')

def peritajes (request):
    return render(request, 'peritajes.html')

def modificarPeritaje (request):
    return render(request, 'modificarPeritaje.html')

def modificarTaller (request):
    return render(request, 'modificarTaller.html')

def modificarMantenimiento (request):
    return render(request, 'modificarMantenimiento.html')
