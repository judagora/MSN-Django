from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario
from django.core.exceptions import ValidationError

class RegistroMecanicoForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo_electronico', 'nombre_usuario', 'telefono', 'password']

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'correo_electronico': 'Correo Electrónico',
            'nombre_usuario': 'Nombre de Usuario',
            'telefono': 'Teléfono',
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
            'password': {
                'required': "El campo contraseña es obligatoria.",
                'min_length': "La contraseña debe tener al menos 8 caracteres."
            },
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password and password.isnumeric():
            raise ValidationError("La contraseña no puede ser solo números. Agrega letras y caracteres especiales.")

        return password



