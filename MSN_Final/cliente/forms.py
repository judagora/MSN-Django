from django import forms
from inicio.models import Vehiculo, Usuario, Soat, Cliente
from datetime import datetime

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
        instance = self.instance
        # Verifica si la placa ya está registrada en la base de datos
        if Vehiculo.objects.filter(placa=placa).exclude(id_vehiculo=instance.id_vehiculo).exists():
            raise forms.ValidationError("Ya existe un vehículo registrado con esta placa.")

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
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'valor_soat': forms.NumberInput(attrs={'min': 0}),
        }

        error_messages = {
            'numero_poliza': {
                'required': "El número de póliza es obligatorio.",
                'max_length': "El número de póliza no puede tener más de 50 caracteres.",
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