from abc import ABC, abstractmethod
from typing import List, Optional

from Domain.Entities.recipe import Recipe

class IRecipeRepository(ABC):
    """Interfaz (ABC) para el repositorio de recetas."""

    @abstractmethod
    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Obtiene una receta por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Recipe]:
        """Obtiene todas las recetas."""
        pass

    @abstractmethod
    def add_recipe(self, recipe: Recipe) -> None:
        """Añade una nueva receta al repositorio."""
        pass

