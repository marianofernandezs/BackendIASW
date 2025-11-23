from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

from domain.entities import Entity, Message, ChatSession, User, Item, CraftingRecipe

T = TypeVar('T', bound=Entity)

class IRepository(ABC, Generic[T]):
    """Interfaz base genérica para repositorios de entidades."""
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def save(self, entity: T):
        """Guarda o actualiza una entidad."""
        pass

    @abstractmethod
    def delete(self, entity_id: str):
        """Elimina una entidad por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        """Obtiene todas las entidades."""
        pass

class IMessageRepository(IRepository[ChatSession], ABC):
    """Interfaz para la persistencia de sesiones y mensajes de chat."""
    @abstractmethod
    def get_session_by_user_id(self, user_id: str) -> Optional[ChatSession]:
        """Obtiene una sesión de chat activa para un usuario."""
        pass

class IUserRepository(IRepository[User], ABC):
    """Interfaz para la persistencia de usuarios."""
    pass

class IInventoryRepository(IRepository[Item], ABC):
    """Placeholder: Interfaz para la persistencia de items de inventario."""
    pass

class ICraftingRepository(IRepository[CraftingRecipe], ABC):
    """Placeholder: Interfaz para la persistencia de recetas de crafteo."""
    pass
