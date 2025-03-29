from django import forms
from django.contrib.auth.forms import UserCreationForm
from inicio.models import Usuario
from django.contrib.auth.forms import PasswordChangeForm
from inicio.models import TallerMecanico
from django.core.exceptions import ValidationError


class ModificarMecanicoForm(forms.ModelForm):
    horario_de_trabajo = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Horario de Trabajo"
    )
    experiencia_laboral = forms.CharField(
        widget=forms.Textarea,
        label="Experiencia Laboral"
    )
    rol_usuario = forms.CharField(
        initial="Mecánico",
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo_electronico', 'nombre_usuario', 'telefono', 'rol_usuario']

class TallerMecanicoForm(forms.ModelForm):
    class Meta:
        model = TallerMecanico
        fields = ['nombre', 'direccion', 'telefono', 'horario_de_atencion', 'id_administrador']
        widgets = {
            'horario_de_atencion': forms.TextInput(attrs={
                'type': 'time',
                'min': '07:00',
                'max': '20:00',
                'step': '1800'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['horario_de_atencion'].widget.attrs.update({'class': 'form-control'})
        self.fields['id_administrador'].widget.attrs.update({'class': 'form-select'})
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if TallerMecanico.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este nombre de taller ya está registrado')
        return nombre
    
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if TallerMecanico.objects.filter(direccion__iexact=direccion).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Esta dirección ya está registrada para otro taller')
        return direccion
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if TallerMecanico.objects.filter(telefono=telefono).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este teléfono ya está registrado para otro taller')
        return telefono


class CambiarContraseñaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los campos si es necesario
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})
    


class RegistroMecanicoForm(UserCreationForm):
    horario_de_trabajo = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'format': '%H:%M'}),
        label="Horario de Trabajo"
    )
    experiencia_laboral = forms.CharField(
        widget=forms.Textarea,
        label="Experiencia Laboral"
    )
    rol_usuario = forms.CharField(
        initial="Mecanico",
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo_electronico', 'nombre_usuario', 'telefono', 'password1', 'password2', 'rol_usuario']

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'correo_electronico': 'Correo Electrónico',
            'nombre_usuario': 'Nombre de Usuario',
            'telefono': 'Teléfono',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

        error_messages = {
            'nombres': {
                'required': "El campo nombre es obligatorio.",
                'max_length': "El campo nombre no puede tener más de 30 caracteres."
            },
            'apellidos': {
                'required': "El campo apellido es obligatorio.",
                'max_length': "El apellido no puede tener más de 30 caracteres."
            },
            'correo_electronico': {
                'required': "El campo correo electrónico es obligatorio.",
                'invalid': "Introduce un correo válido.",
                'unique': "Este correo ya está registrado. Usa otro."
            },
            'nombre_usuario': {
                'required': "El campo nombre de usuario es obligatorio.",
                'max_length': "El nombre de usuario no puede exceder 30 caracteres.",
                'unique': "Este nombre de usuario ya está en uso."
            },
            'telefono': {
                'required': "El campo teléfono es obligatorio.",
                'min_length': "El teléfono debe tener al menos 10 dígitos.",
                'max_length': "El teléfono no puede tener más de 10 dígitos."
            },
            'password1': {
                'required': "La contraseña es obligatoria.",
                'min_length': "La contraseña debe tener al menos 8 caracteres."
            },
            'password2': {
                'required': "Debes confirmar tu contraseña."
            }
        }


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol_usuario = "Mecanico"
        if commit:
            usuario.save()
        return usuario
    

    