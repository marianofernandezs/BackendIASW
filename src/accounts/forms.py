from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserRegistrationForm(forms.Form):
    """Formulario para registrar nuevos usuarios."""

    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'})
    )

    password = forms.CharField(
        label="Contraseña",
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres'})
    )

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput()
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener mínimo 8 caracteres.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Debe contener al menos una mayúscula.")
        if not re.search(r"\d", password):
            raise ValidationError("Debe contener al menos un número.")
        return password

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password_confirm"):
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned
