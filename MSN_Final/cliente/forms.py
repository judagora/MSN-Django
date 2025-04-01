from django import forms
from inicio.models import Vehiculo, Usuario, Soat, Cliente, Notificaciones, MantenimientoProgramado
from datetime import datetime, time, timedelta
from django.core.exceptions import ValidationError
import re

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['modelo', 'tipo', 'marca', 'placa', 'color', 'kilometraje']
        widgets = {
            'modelo': forms.NumberInput(attrs={'placeholder': 'Ej: 2023', 'minlength': '4', 'maxlength': '4'}),
            'tipo': forms.Select(attrs={'id': 'tipoLista'}),
            'marca': forms.TextInput(attrs={'maxlength': '10', 'minlength': '3'}),
            'placa': forms.TextInput(attrs={'maxlength': '6', 'minlength': '6', 'placeholder': 'Ej: AAA123'}),
            'color': forms.TextInput(attrs={'placeholder': 'Ej: Azul'}),
            'kilometraje': forms.NumberInput(attrs={'minlength': '1', 'maxlength': '6', 'placeholder': '15000'}),
        }

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')

        # Verifica que tenga exactamente 4 dígitos
        if not modelo.isdigit() or len(modelo) != 4:
            raise forms.ValidationError("El modelo debe tener exactamente 4 dígitos numéricos.")

        # Verifica que no sea menor al año 1900 ni mayor al actual
        año_actual = datetime.now().year
        if int(modelo) < 1900 or int(modelo) > año_actual:
            raise forms.ValidationError(f"El modelo debe estar entre 1900 y {año_actual}.")

        return modelo
    
    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        tipo = self.cleaned_data.get('tipo')  # Asegúrate de que 'tipo' es un campo válido en tu modelo

        # Expresiones regulares para validar el formato
        regex_carro = r'^[A-Z]{3}\d{3}$'    # Formato: AAA123
        regex_moto = r'^[A-Z]{3}\d{2}[A-Z]$'  # Formato: AAA12T

        if tipo == "Automovil" or tipo == "Camioneta":  # Ajusta según los valores que uses en 'tipo'
            if not re.fullmatch(regex_carro, placa):
                raise ValidationError("Formato de placa incorrecto. Para carros: AAA123.")
        elif tipo == "Motocicleta":
            if not re.fullmatch(regex_moto, placa):
                raise ValidationError("Formato de placa incorrecto. Para motos: AAA12T.")
        else:
            raise ValidationError("Tipo de vehículo no válido.")

        # Verificar si ya existe en la base de datos (evitando duplicados)
        instance = self.instance
        if Vehiculo.objects.filter(placa=placa).exclude(id_vehiculo=instance.id_vehiculo).exists():
            raise ValidationError("Ya existe un vehículo registrado con esta placa.")

        return placa
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo_electronico', 'nombre_usuario', 'telefono']


        error_messages = {
            'nombres': {
                'required': "El nombre es obligatorio.",
                'max_length': "El nombre no puede tener más de 30 caracteres."
            },
            'apellidos': {
                'required': "El apellido es obligatorio.",
                'max_length': "El apellido no puede tener más de 30 caracteres."
            },
            'correo_electronico': {
                'required': "El correo es obligatorio.",
                'max_length': "El correo no puede exceder 50 caracteres.",
                'unique': "Este correo ya está en uso."
            },
            'nombre_usuario': {
                'required': "El nombre de usuario es obligatorio.",
                'max_length': "El nombre de usuario no puede exceder 30 caracteres.",
                'unique': "Este nombre de usuario ya está en uso."
            },
            'telefono': {
                'required': "El teléfono es obligatorio.",
                'min_length': "El teléfono debe tener al menos 10 dígitos.",
                'max_length': "El teléfono no puede tener más de 10 dígitos.",
                'unique': "Este teléfono ya está en uso."
            }
        }
        
    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        if not correo:
            raise forms.ValidationError("El correo es obligatorio.")

        usuario_id = self.instance.id_usuario if self.instance and hasattr(self.instance, 'id_usuario') else None
    
        if Usuario.objects.filter(correo_electronico=correo).exclude(id_usuario=usuario_id).exists():
            raise forms.ValidationError("Este correo ya está registrado. Usa otro.")

        return correo
    

class SoatForm(forms.ModelForm):
    class Meta:
        model = Soat
        fields = ['numero_poliza', 'fecha_emision', 'fecha_vencimiento', 'valor_soat', 'aseguradora', 'id_vehiculo']


        error_messages = {
            'numero_poliza': {
                'required': "El número de póliza es obligatorio.",
                'max_length': "El número de póliza no puede tener más de 20 caracteres.",
                'min_length': "El número de póliza debe tener al menos 10 caracteres.",
                'unique': "Este número de póliza ya está registrado.",
            },
            'fecha_emision': {
                'required': "La fecha de emisión es obligatoria.",
                'invalid': "Ingrese una fecha de emisión válida.",
            },
            'fecha_vencimiento': {
                'required': "La fecha de vencimiento es obligatoria.",
                'invalid': "Ingrese una fecha de vencimiento válida.",
                'future_date': "La fecha de vencimiento debe ser posterior a la fecha de emisión.",
            },
            'valor_soat': {
                'required': "El valor del SOAT es obligatorio.",
                'invalid': "Ingrese un valor numérico válido.",
                'min_value': "El valor del SOAT debe ser mayor a 0.",
            },
            'aseguradora': {
                'required': "El nombre de la aseguradora es obligatorio.",
                'max_length': "El nombre de la aseguradora no puede superar los 50 caracteres.",
            },
            'id_vehiculo': {
                'required': "Debe seleccionar un vehículo.",
                'invalid_choice': "Seleccione un vehículo válido.",
            },
            


        }

    def __init__(self, *args, cliente=None, **kwargs):
        super(SoatForm, self).__init__(*args, **kwargs)
        if cliente:
            self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(id_cliente=cliente)

    def clean_id_vehiculo(self):
        id_vehiculo = self.cleaned_data.get('id_vehiculo')
        if self.instance.pk:
            if Soat.objects.filter(id_vehiculo=id_vehiculo).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Este vehículo ya tiene un SOAT registrado.")
        else:
            if Soat.objects.filter(id_vehiculo=id_vehiculo).exists():
                raise ValidationError("Este vehículo ya tiene un SOAT registrado.")
        return id_vehiculo
    
    def clean_valor_soat(self):
        valor_soat = self.cleaned_data.get('valor_soat')

        if not re.fullmatch(r'\d+', str(valor_soat)):
            raise ValidationError("Introducir el valor sin puntos ni comas.")

        # Validar el rango permitido
        if valor_soat < 100000 or valor_soat > 1400000:
            raise ValidationError("El valor del SOAT debe estar entre $100,000 y $1,400,000.")

        return valor_soat
    
    def clean_numero_poliza(self):
        numero_poliza = self.cleaned_data.get('numero_poliza')

        # Verificar que solo contenga números y tenga entre 15 y 20 dígitos
        if not re.fullmatch(r'\d{15,20}', str(numero_poliza)):
            raise ValidationError("El número de póliza debe contener entre 15 y 20 dígitos numéricos.")

        return numero_poliza
    
    def clean_fecha_emision(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        annio_actual = datetime.now().year
        if fecha_emision.year < annio_actual-1:
            raise ValidationError(f"La fecha de emisión no puede ser menor a {annio_actual-1}.")
        return fecha_emision
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get("fecha_emision")
        fecha_vencimiento = cleaned_data.get("fecha_vencimiento")

        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento != fecha_emision.replace(year=fecha_emision.year + 1):
                raise ValidationError({
                    "fecha_vencimiento": "La fecha de vencimiento debe ser exactamente un año después de la fecha de emisión."
                })

        return cleaned_data
    
class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificaciones
        fields = ['motivo', 'fecha_recordatorio', 'hora_recordatorio', 'notas']

    def clean_fecha_recordatorio(self):
        fecha = self.cleaned_data.get('fecha_recordatorio')
        if fecha and fecha < datetime.today().date():
            raise ValidationError("La fecha no puede ser anterior al día actual.")
        return fecha

    def clean_hora_recordatorio(self):
        hora = self.cleaned_data.get('hora_recordatorio')
        hora_minima = time(6, 0)  # 6:00 AM
        hora_maxima = time(19, 0) # 7:00 PM

        if hora and (hora < hora_minima or hora > hora_maxima):
            raise ValidationError("La hora debe estar entre las 6:00 AM y las 7:00 PM.")
        return hora
    

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoProgramado
        fields = ['tipo_Mantenimiento', 'id_mecanico', 'id_vehiculo', 'id_taller_mecanico', 'fecha_mantenimiento', 'hora_mantenimiento', 'notas']

        error_messages = {
            'tipo_Mantenimiento': {
                'required': "El tipo de mantenimiento es obligatorio.",
            },
            'id_mecanico': {
                'required': "Debes seleccionar un mecánico.",
                'invalid_choice': "El mecánico seleccionado no es válido."
            },
            'id_vehiculo': {
                'required': "Debes seleccionar un vehículo.",
                'invalid_choice': "El vehículo seleccionado no es válido."
            },
            'id_taller_mecanico': {
                'required': "Debes seleccionar un taller mecánico.",
                'invalid_choice': "El taller mecánico seleccionado no es válido."
            },
            'fecha_mantenimiento': {
                'required': "La fecha del mantenimiento es obligatoria.",
                'invalid': "Ingresa una fecha válida."
            },
            'hora_mantenimiento': {
                'required': "La hora del mantenimiento es obligatoria.",
                'invalid': "Ingresa una hora válida (HH:MM)."
            },
            'notas': {
                'max_length': "Las notas no pueden tener más de 100 caracteres.",
            }
        }
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha_mantenimiento')
        hora = cleaned_data.get('hora_mantenimiento')
        mecanico = cleaned_data.get('id_mecanico')

        if not (fecha and hora and mecanico):
            return cleaned_data  # Si falta algún campo, no validar más.

        # Verificar si el mecánico ya tiene 4 mantenimientos en ese día**
        mantenimientos_mismo_dia = MantenimientoProgramado.objects.filter(
            id_mecanico=mecanico,
            fecha_mantenimiento=fecha
        )

        if mantenimientos_mismo_dia.count() >= 4:
            self.add_error('fecha_mantenimiento', "Este mecánico ya tiene varios mantenimientos programados para este día, Por favor, selecciona otro día.")

        # Verificar si la hora ya está ocupada (solo se permite cada 3 horas)**
        tres_horas = timedelta(hours=3)

        for mantenimiento in mantenimientos_mismo_dia:
            diferencia_horas = abs(mantenimiento.hora_mantenimiento.hour - hora.hour)
            if diferencia_horas < 3:  # Si la diferencia es menor a 3 horas
                self.add_error('hora_mantenimiento', "Ya hay un mantenimiento programado en esa franja horaria. Seleccione otra hora (3 horas de diferencia).")

        return cleaned_data
        
