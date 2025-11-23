from typing import List, Optional, Dict

from Application.Interfaces.category_repository import ICategoryRepository
from Domain.Entities.category import Category
from Domain.Exceptions.custom_exceptions import CategoryNotFoundException

class InMemoryCategoryRepository(ICategoryRepository):
    """Implementación en memoria del repositorio de categorías."""

    def __init__(self, initial_categories: Optional[List[Category]] = None):
        self._categories: Dict[str, Category] = {}
        if initial_categories:
            for category in initial_categories:
                self._categories[category.id] = category

    def get_by_id(self, category_id: str) -> Optional[Category]:
        """Obtiene una categoría por su ID."""
        return self._categories.get(category_id)

    def get_all(self) -> List[Category]:
        """Obtiene todas las categorías."""
        return list(self._categories.values())

    def add_category(self, category: Category) -> None:
        """Añade una nueva categoría al repositorio."""
        if category.id in self._categories:
            print(f"Advertencia: Categoría con ID {category.id} ya existe. Sobrescribiendo.")
        self._categories[category.id] = category

