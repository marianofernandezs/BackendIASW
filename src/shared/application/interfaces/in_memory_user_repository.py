from typing import Dict, Optional

from Assets.Scripts.domain.entities.user import User
from Assets.Scripts.domain.repositories.user_repository import IUserRepository
from Assets.Scripts.domain.value_objects.email import Email

class InMemoryUserRepository(IUserRepository):
    """
    Implementación en memoria del IUserRepository.
    Útil para pruebas o prototipos sin una base de datos real.
    """
    _users: Dict[str, User] = {} # Key: email.value, Value: User object

    def __init__(self):
        """Inicializa el repositorio en memoria."""
        self._users = {}

    def save(self, user: User) -> User:
        """
        Guarda un usuario en la "base de datos" en memoria.
        Asume que si el email ya existe, lo actualiza (simplicidad).
        """
        self._users[user.email.value] = user
        return user

    def get_by_email(self, email: Email) -> Optional[User]:
        """
        Obtiene un usuario por email de la "base de datos" en memoria.
        """
        return self._users.get(email.value)

    def email_exists(self, email: Email) -> bool:
        """
        Verifica si un email existe en la "base de datos" en memoria.
        """
        return email.value in self._users

    def reset(self):
        """Reinicia el repositorio para pruebas."""
        self._users = {}
