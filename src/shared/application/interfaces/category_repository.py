from abc import ABC, abstractmethod
from typing import List, Optional

from Domain.Entities.category import Category

class ICategoryRepository(ABC):
    """Interfaz (ABC) para el repositorio de categorías."""

    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[Category]:
        """Obtiene una categoría por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Category]:
        """Obtiene todas las categorías."""
        pass

    @abstractmethod
    def add_category(self, category: Category) -> None:
        """Añade una nueva categoría al repositorio."""
        pass

