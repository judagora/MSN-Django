from django.shortcuts import render

def inicio(request):
    return render(request, 'indexMecanico.html')

def insertarMantenimiento (request):
    return render(request, 'insertarMantenimiento.html')

def modificarMantenimiento (request):
    return render(request, 'modificarMantenimiento.html')

def modificarMantenimiento2 (request):
    return render(request, 'modificarMantenimiento2.html')

def consultarMantenimiento (request):
    return render(request, 'consultarMantenimiento.html')

def consultarMantenimiento2 (request):
    return render(request, 'consultarMantenimiento2.html')

def insertarPeritaje (request):
    return render(request, 'insertarPeritaje.html')

def modificarPeritaje (request):
    return render(request, 'modificarPeritaje.html')

def modificarPeritaje2 (request):
    return render(request, 'modificarPeritaje2.html')

def consultarPeritaje (request):
    return render(request, 'consultarPeritaje.html')

def consultarPeritaje2 (request):
    return render(request, 'consultarPeritaje2.html')

def insertarRepuesto (request):
    return render(request, 'insertarRepuesto.html')

def modificarRepuesto (request):
    return render(request, 'modificarRepuesto.html')

def modificarRepuesto2 (request):
    return render(request, 'modificarRepuesto2.html')

def consultarRepuesto (request):
    return render(request, 'consultarRepuesto.html')

def consultarRepuesto2 (request):
    return render(request, 'consultarRepuesto2.html')

