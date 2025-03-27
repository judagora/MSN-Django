from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from inicio.models import Mantenimiento, Vehiculo, VehiculoMantenimiento, Peritaje, VehiculoPeritaje, VehiculoRepuestosModificados, RepuestosModificados, Mecanico, MecanicoMantenimiento, MecanicoPeritaje, MecanicoRepuestosModificados 
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    # Obtener el mecánico actual
    mecanico = None
    if request.user.is_authenticated:
        try:
            mecanico = Mecanico.objects.get(id_usuario=request.user)
        except Mecanico.DoesNotExist:
            pass
    
    context = {
        'user': request.user,
        'mecanico': mecanico
    }
    
    if mecanico:
        # Optimización: Obtenemos todos los datos necesarios en menos consultas
        # Estadísticas de MANTENIMIENTOS
        mantenimientos_mecanico = MecanicoMantenimiento.objects.filter(
            id_mecanico=mecanico
        ).select_related('id_mantenimiento').prefetch_related(
            'id_mantenimiento__vehiculomantenimiento_set__id_vehiculo'
        )
        
        # Preparamos datos para gráficos y estadísticas
        if mantenimientos_mecanico.exists():
            # Vehículos únicos con mantenimientos
            vehiculos_mantenimiento = VehiculoMantenimiento.objects.filter(
                id_mantenimiento__in=[m.id_mantenimiento for m in mantenimientos_mecanico]
            ).values('id_vehiculo').distinct().count()
            
            # Mantenimientos por tipo (optimizado)
            mantenimientos_por_tipo = Mantenimiento.objects.filter(
                id_mantenimiento__in=[m.id_mantenimiento.id_mantenimiento for m in mantenimientos_mecanico]
            ).values('tipo_mantenimiento').annotate(total=Count('id_mantenimiento'))
            
            # Últimos 5 mantenimientos ordenados por ID descendente
            ultimos_mantenimientos = mantenimientos_mecanico.order_by('-id_mantenimiento__id_mantenimiento')[:5]
            
            context.update({
                'total_mantenimientos': mantenimientos_mecanico.count(),
                'vehiculos_mantenimiento': vehiculos_mantenimiento,
                'mantenimientos_por_tipo': list(mantenimientos_por_tipo),
                'ultimos_mantenimientos': ultimos_mantenimientos,
            })
        
        # Estadísticas de PERITAJES (optimizadas)
        peritajes_mecanico = MecanicoPeritaje.objects.filter(
            id_mecanico=mecanico
        ).select_related('id_peritaje').prefetch_related(
            'id_peritaje__vehiculoperitaje_set__id_vehiculo'
        )
        
        if peritajes_mecanico.exists():
            # Vehículos únicos con peritajes
            vehiculos_peritaje = VehiculoPeritaje.objects.filter(
                id_peritaje__in=[p.id_peritaje for p in peritajes_mecanico]
            ).values('id_vehiculo').distinct().count()
            
            # Peritajes por tipo (aunque en el modelo no hay tipo, mantenemos la estructura)
            peritajes_por_tipo = Peritaje.objects.filter(
                id_peritaje__in=[p.id_peritaje.id_peritaje for p in peritajes_mecanico]
            ).extra(select={'tipo': "'Peritaje'"}).values('tipo').annotate(total=Count('id_peritaje'))
            
            # Últimos 5 peritajes ordenados por ID descendente
            ultimos_peritajes = peritajes_mecanico.order_by('-id_peritaje__id_peritaje')[:5]
            
            context.update({
                'total_peritajes': peritajes_mecanico.count(),
                'vehiculos_peritaje': vehiculos_peritaje,
                'peritajes_por_tipo': list(peritajes_por_tipo),
                'ultimos_peritajes': ultimos_peritajes,
            })
    
    return render(request, 'indexMecanicoMc.html', context)

@login_required
def insertarMantenimientoMc(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        placa = request.POST.get('placa')
        tipo_mantenimiento = request.POST.get('tipoMantenimiento')
        descripcion = request.POST.get('descripcionMantenimiento')
        costo = request.POST.get('costoMantenimiento')
        notas_adicionales = request.POST.get('notasAdicionalesMantenimiento')

        try:
            # Validar que el costo sea un número válido
            costo = float(costo)
            print(f'Costo recibido: {costo}')  # Depuración

            if costo < 50000:  # Permite 50,000 exactos
                raise ValidationError('El costo debe ser igual o mayor a 50,000.')

            # Buscar el vehículo por placa
            vehiculo = Vehiculo.objects.get(placa=placa)

            # Crear el mantenimiento
            mantenimiento = Mantenimiento(
                tipo_mantenimiento=tipo_mantenimiento,
                descripcion=descripcion,
                costo=costo,
                notas_adicionales=notas_adicionales
            )
            mantenimiento.full_clean()  # Validar el modelo
            mantenimiento.save()

            # Actualizar el campo id_mantenimiento en el vehículo
            vehiculo.id_mantenimiento = mantenimiento
            vehiculo.save()

            # Asociar el mantenimiento al vehículo en la tabla VehiculoMantenimiento
            VehiculoMantenimiento.objects.create(
                id_vehiculo=vehiculo,
                id_mantenimiento=mantenimiento
            )

            # Obtener el mecánico asociado al usuario autenticado
            usuario_actual = request.user  # Usuario autenticado
            mecanico = Mecanico.objects.get(id_usuario=usuario_actual)

            # Asociar el mantenimiento al mecánico en la tabla MecanicoMantenimiento
            MecanicoMantenimiento.objects.create(
                id_mecanico=mecanico,
                id_mantenimiento=mantenimiento
            )

            # Mensaje de éxito
            messages.success(request, 'Mantenimiento registrado correctamente.')
            return redirect('mecanico:modificarMantenimientoMc')
        except Vehiculo.DoesNotExist:
            # Mensaje de error si el vehículo no existe
            messages.error(request, 'El vehículo con la placa proporcionada no existe.')
        except Mecanico.DoesNotExist:
            # Mensaje de error si el usuario no es un mecánico
            messages.error(request, 'El usuario autenticado no está asociado a un mecánico.')
        except ValidationError as e:
            # Mensaje de error si el costo no es válido
            messages.error(request, str(e))
        except ValueError:
            # Mensaje de error si el costo no es un número válido
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            # Mensaje de error genérico
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario
    return render(request, 'insertarMantenimientoMc.html')

@login_required
def verificar_placa(request):
    try:
        placa = request.GET.get('placa')
        if not placa:
            return JsonResponse({'error': 'Placa no proporcionada.'}, status=400)

        exists = Vehiculo.objects.filter(placa=placa).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def consultarMantenimientoMc(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        if placa:
            return redirect('mecanico:consultarMantenimientoMc2', placa=placa)
    
    return render(request, 'consultarMantenimientoMc.html')

@login_required
def consultarMantenimientoMc2(request, placa):
    # Buscar el vehículo por placa
    vehiculo = get_object_or_404(Vehiculo, placa=placa)

    # Obtener todos los mantenimientos asociados al vehículo a través de la tabla intermedia
    mantenimientos = VehiculoMantenimiento.objects.filter(id_vehiculo=vehiculo).select_related('id_mantenimiento')

    if not mantenimientos:
        # Si no hay mantenimientos asociados, mostrar un mensaje
        return render(request, 'consultarMantenimientoMc2.html', {
            'placa': placa,
            'mensaje': 'No se encontraron mantenimientos para este vehículo.'
        })

    # Pasar todos los mantenimientos a la plantilla
    return render(request, 'consultarMantenimientoMc2.html', {
        'placa': placa,
        'mantenimientos': mantenimientos,  # Pasar todos los mantenimientos
    })

@login_required
def modificarMantenimientoMc(request):
    # Obtener todos los registros de VehiculoMantenimiento con sus relaciones
    vehiculo_mantenimientos = VehiculoMantenimiento.objects.select_related('id_vehiculo', 'id_mantenimiento').all()

    # Renderizar la plantilla con los datos
    return render(request, 'modificarMantenimientoMc.html', {
        'vehiculo_mantenimientos': vehiculo_mantenimientos,
    })

@login_required
def modificarMantenimientoMc2(request, placa, id_mantenimiento):
    # Obtener el mantenimiento específico por placa e ID del mantenimiento
    vehiculo_mantenimiento = get_object_or_404(
        VehiculoMantenimiento,
        id_vehiculo__placa=placa,
        id_mantenimiento__id_mantenimiento=id_mantenimiento
    )
    mantenimiento = vehiculo_mantenimiento.id_mantenimiento

    if request.method == 'POST':
        try:
            # Procesar el formulario y guardar los cambios
            tipo_mantenimiento = request.POST.get('tipo_mantenimiento')
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costo')
            notas_adicionales = request.POST.get('notas_adicionales')

            # Validar el costo
            costo = float(costo)
            if costo < 50000:
                raise ValidationError('El costo debe ser igual o mayor a 50,000.')

            # Actualizar los campos del mantenimiento
            mantenimiento.tipo_mantenimiento = tipo_mantenimiento
            mantenimiento.descripcion = descripcion
            mantenimiento.costo = costo
            mantenimiento.notas_adicionales = notas_adicionales

            # Guardar los cambios
            mantenimiento.full_clean()  # Validar el modelo
            mantenimiento.save()

            # Mensaje de éxito
            messages.success(request, 'Mantenimiento modificado correctamente.')
            return redirect('mecanico:modificarMantenimientoMc')

        except ValidationError as e:
            messages.error(request, str(e))
        except ValueError:
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario con los datos del mantenimiento
    return render(request, 'modificarMantenimientoMc2.html', {
        'mantenimiento': mantenimiento,
        'placa': placa,
    })

@login_required
def insertarPeritajeMc(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        placa = request.POST.get('placa')
        descripcion = request.POST.get('descripcionPeritaje')
        costo = request.POST.get('costoPeritaje')
        notas_adicionales = request.POST.get('notasAdicionalesPeritaje')

        try:
            # Validar que el costo sea un número válido
            costo = float(costo)
            print(f'Costo recibido: {costo}')  # Depuración

            if costo < 50000:  # Permite 50,000 exactos
                raise ValidationError('El costo debe ser igual o mayor a 50,000.')

            # Buscar el vehículo por placa
            vehiculo = Vehiculo.objects.get(placa=placa)

            # Crear el peritaje
            peritaje = Peritaje(
                descripcion=descripcion,
                costo=costo,
                notas_adicionales=notas_adicionales
            )
            peritaje.full_clean()  # Validar el modelo
            peritaje.save()

            # Actualizar el campo id_peritaje en el vehículo
            vehiculo.id_peritaje = peritaje
            vehiculo.save()

            # Asociar el peritaje al vehículo en la tabla VehiculoPeritaje
            VehiculoPeritaje.objects.create(
                id_vehiculo=vehiculo,
                id_peritaje=peritaje
            )

            # Obtener el mecánico asociado al usuario autenticado
            usuario_actual = request.user  # Usuario autenticado
            mecanico = Mecanico.objects.get(id_usuario=usuario_actual)

            # Asociar el peritaje al mecánico en la tabla MecanicoPeritaje
            MecanicoPeritaje.objects.create(
                id_mecanico=mecanico,
                id_peritaje=peritaje
            )

            # Mensaje de éxito
            messages.success(request, 'Peritaje registrado correctamente.')
            return redirect('mecanico:modificarPeritajeMc')
        except Vehiculo.DoesNotExist:
            # Mensaje de error si el vehículo no existe
            messages.error(request, 'El vehículo con la placa proporcionada no existe.')
        except Mecanico.DoesNotExist:
            # Mensaje de error si el usuario no es un mecánico
            messages.error(request, 'El usuario autenticado no está asociado a un mecánico.')
        except ValidationError as e:
            # Mensaje de error si el costo no es válido
            messages.error(request, str(e))
        except ValueError:
            # Mensaje de error si el costo no es un número válido
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            # Mensaje de error genérico
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario
    return render(request, 'insertarPeritajeMc.html')

@login_required
def modificarPeritajeMc(request):
    # Obtener todos los registros de VehiculoPeritaje con sus relaciones
    vehiculo_peritajes = VehiculoPeritaje.objects.select_related('id_vehiculo', 'id_peritaje').all()

    # Renderizar la plantilla con los datos
    return render(request, 'modificarPeritajeMc.html', {
        'vehiculo_peritajes': vehiculo_peritajes,
    })

@login_required
def modificarPeritajeMc2(request, placa, id_peritaje):
    # Obtener el peritaje específico por placa e ID del peritaje
    vehiculo_peritaje = get_object_or_404(
        VehiculoPeritaje,
        id_vehiculo__placa=placa,
        id_peritaje__id_peritaje=id_peritaje
    )
    peritaje = vehiculo_peritaje.id_peritaje

    if request.method == 'POST':
        try:
            # Procesar el formulario y guardar los cambios
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costo')
            notas_adicionales = request.POST.get('notas_adicionales')

            # Validar el costo
            costo = float(costo)
            if costo < 50000:
                raise ValidationError('El costo debe ser igual o mayor a 50,000.')

            # Actualizar los campos del peritaje
            peritaje.descripcion = descripcion
            peritaje.costo = costo
            peritaje.notas_adicionales = notas_adicionales

            # Guardar los cambios
            peritaje.full_clean()  # Validar el modelo
            peritaje.save()

            # Mensaje de éxito
            messages.success(request, 'Peritaje modificado correctamente.')
            return redirect('mecanico:modificarPeritajeMc')

        except ValidationError as e:
            messages.error(request, str(e))
        except ValueError:
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario con los datos del peritaje
    return render(request, 'modificarPeritajeMc2.html', {
        'peritaje': peritaje,
        'placa': placa,
    })

@login_required
def consultarPeritajeMc(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        if placa:
            return redirect('mecanico:consultarPeritajeMc2', placa=placa)
    
    return render(request, 'consultarPeritajeMc.html')

@login_required
def consultarPeritajeMc2(request, placa):
    # Buscar el vehículo por placa
    vehiculo = get_object_or_404(Vehiculo, placa=placa)

    # Obtener todos los peritajes asociados al vehículo a través de la tabla intermedia
    peritajes = VehiculoPeritaje.objects.filter(id_vehiculo=vehiculo).select_related('id_peritaje')

    if not peritajes:
        # Si no hay peritajes asociados, mostrar un mensaje
        return render(request, 'consultarPeritajeMc2.html', {
            'placa': placa,
            'mensaje': 'No se encontraron peritajes para este vehículo.'
        })

    # Pasar todos los peritajes a la plantilla
    return render(request, 'consultarPeritajeMc2.html', {
        'placa': placa,
        'peritajes': peritajes,  # Pasar todos los peritajes
    })

@login_required
def insertarRepuestoMc(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        placa = request.POST.get('placa')
        descripcion = request.POST.get('descripcionRepuesto')
        motivo = request.POST.get('motivoRepuesto')
        costo = request.POST.get('costoRepuesto')

        try:
            # Validar que el costo sea un número válido
            costo = float(costo)
            print(f'Costo recibido: {costo}')  # Depuración

            if costo < 10000:  # Permite 10,000 exactos
                raise ValidationError('El costo debe ser igual o mayor a 10,000.')

            # Buscar el vehículo por placa
            vehiculo = Vehiculo.objects.get(placa=placa)

            # Crear el repuesto modificado
            repuesto_modificado = RepuestosModificados(
                descripcion=descripcion,
                motivo=motivo,
                costo=costo
            )
            repuesto_modificado.full_clean()  # Validar el modelo
            repuesto_modificado.save()

            # Actualizar el campo id_repuestos_modificados en el vehículo
            vehiculo.id_repuestos_modificados = repuesto_modificado
            vehiculo.save()

            # Asociar el repuesto modificado al vehículo en la tabla VehiculoRepuestosModificados
            VehiculoRepuestosModificados.objects.create(
                id_vehiculo=vehiculo,
                id_repuestos_modificados=repuesto_modificado
            )

            # Obtener el mecánico asociado al usuario autenticado
            usuario_actual = request.user  # Usuario autenticado
            mecanico = Mecanico.objects.get(id_usuario=usuario_actual)

            # Asociar el repuesto modificado al mecánico en la tabla MecanicoRepuestosModificados
            MecanicoRepuestosModificados.objects.create(
                id_mecanico=mecanico,
                id_repuestos_modificados=repuesto_modificado
            )

            # Mensaje de éxito
            messages.success(request, 'Repuesto modificado registrado correctamente.')
            return redirect('mecanico:modificarRepuestoMc')
        except Vehiculo.DoesNotExist:
            # Mensaje de error si el vehículo no existe
            messages.error(request, 'El vehículo con la placa proporcionada no existe.')
        except Mecanico.DoesNotExist:
            # Mensaje de error si el usuario no es un mecánico
            messages.error(request, 'El usuario autenticado no está asociado a un mecánico.')
        except ValidationError as e:
            # Mensaje de error si el costo no es válido
            messages.error(request, str(e))
        except ValueError:
            # Mensaje de error si el costo no es un número válido
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            # Mensaje de error genérico
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario
    return render(request, 'insertarRepuestoMc.html')

@login_required
def modificarRepuestoMc(request):
    # Obtener todos los registros de VehiculoRepuestosModificados con sus relaciones
    vehiculo_repuestos = VehiculoRepuestosModificados.objects.select_related('id_vehiculo', 'id_repuestos_modificados').all()

    # Renderizar la plantilla con los datos
    return render(request, 'modificarRepuestoMc.html', {
        'vehiculo_repuestos': vehiculo_repuestos,
    })

@login_required
def modificarRepuestoMc2(request, placa, id_repuesto):
    # Obtener el repuesto específico por placa e ID del repuesto
    vehiculo_repuesto = get_object_or_404(
        VehiculoRepuestosModificados,
        id_vehiculo__placa=placa,
        id_repuestos_modificados__id_repuestos_modificados=id_repuesto
    )
    repuesto = vehiculo_repuesto.id_repuestos_modificados

    if request.method == 'POST':
        try:
            # Procesar el formulario y guardar los cambios
            descripcion = request.POST.get('descripcion')
            motivo = request.POST.get('motivo')
            costo = request.POST.get('costo')

            # Validar el costo
            costo = float(costo)
            if costo < 0:
                raise ValidationError('El costo debe ser un número válido.')

            # Actualizar los campos del repuesto
            repuesto.descripcion = descripcion
            repuesto.motivo = motivo
            repuesto.costo = costo

            # Guardar los cambios
            repuesto.full_clean()  # Validar el modelo
            repuesto.save()

            # Mensaje de éxito
            messages.success(request, 'Repuesto modificado correctamente.')
            return redirect('mecanico:modificarRepuestoMc')

        except ValidationError as e:
            messages.error(request, str(e))
        except ValueError:
            messages.error(request, 'El costo debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')

    # Renderizar el formulario con los datos del repuesto
    return render(request, 'modificarRepuestoMc2.html', {
        'repuesto': repuesto,
        'placa': placa,
    })

@login_required
def consultarRepuestoMc(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        if placa:
            return redirect('mecanico:consultarRepuestoMc2', placa=placa)
    
    return render(request, 'consultarRepuestoMc.html')

@login_required
def consultarRepuestoMc2(request, placa):
    # Buscar el vehículo por placa
    vehiculo = get_object_or_404(Vehiculo, placa=placa)

    # Obtener todos los repuestos modificados asociados al vehículo a través de la tabla intermedia
    repuestos_modificados = VehiculoRepuestosModificados.objects.filter(id_vehiculo=vehiculo).select_related('id_repuestos_modificados')

    if not repuestos_modificados:
        # Si no hay repuestos modificados asociados, mostrar un mensaje
        return render(request, 'consultarRepuestoMc2.html', {
            'placa': placa,
            'mensaje': 'No se encontraron repuestos modificados para este vehículo.'
        })

    # Pasar todos los repuestos modificados a la plantilla
    return render(request, 'consultarRepuestoMc2.html', {
        'placa': placa,
        'repuestos_modificados': repuestos_modificados,  # Pasar todos los repuestos modificados
    })

