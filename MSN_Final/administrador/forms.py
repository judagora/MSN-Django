from django import forms
from django.contrib.auth.forms import UserCreationForm
from inicio.models import Usuario


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
        }


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol_usuario = "Mecanico"
        if commit:
            usuario.save()
        return usuario
    

    