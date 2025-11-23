from abc import ABC, abstractmethod
from typing import Optional

from Assets.Scripts.domain.entities.user import User
from Assets.Scripts.domain.value_objects.email import Email

class IUserRepository(ABC):
    """
    Interfaz abstracta para el repositorio de usuarios.
    Define el contrato para la persistencia de entidades User.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guarda o actualiza un usuario en el repositorio.
        :param user: La entidad User a guardar.
        :return: La entidad User guardada (puede tener un ID asignado si es nuevo).
        """
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        """
        Obtiene un usuario por su dirección de email.
        :param email: Objeto Email del usuario.
        :return: La entidad User si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def email_exists(self, email: Email) -> bool:
        """
        Verifica si ya existe un usuario con el email dado.
        :param email: Objeto Email a verificar.
        :return: True si el email ya está en uso, False en caso contrario.
        """
        pass
