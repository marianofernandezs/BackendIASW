from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class UserAccountService:
    """Servicio de lógica de negocio para cuentas de usuario."""

    @staticmethod
    @transaction.atomic
    def register_user(email: str, password: str) -> User:
        username = email.split("@")[0]  # Crear username básico
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
