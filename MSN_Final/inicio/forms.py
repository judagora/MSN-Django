from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'correo_electronico', 'nombre_usuario', 'telefono', 'password1', 'password2']

        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'correo_electronico': 'Correo Electrónico',
            'nombre_usuario': 'Nombre de Usuario',
            'telefono': 'Teléfono',
        }
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
                'required': "El correo electrónico es obligatorio.",
                'invalid': "Introduce un correo válido.",
                'unique': "Este correo ya está registrado. Usa otro."
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
            },
            'password1': {
                'required': "La contraseña es obligatoria.",
                'min_length': "La contraseña debe tener al menos 8 caracteres."
            },
            'password2': {
                'required': "Debes confirmar tu contraseña."
            }
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if password1 and password1.isnumeric():
            raise ValidationError("La contraseña no puede ser solo números. Agrega letras y caracteres especiales.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")


        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Asegúrate de escribirlas correctamente.")
        
        if password2 and password2.isnumeric():
            raise ValidationError("La contraseña no puede ser solo números. Agrega letras y caracteres especiales.")
        return password2

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Correo Electrónico"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"})
    )

    error_messages = {
        'invalid_login': "Correo o contraseña incorrectos. Inténtalo de nuevo.",
        'inactive': "Tu cuenta está inactiva. Contacta al administrador."
    }
    