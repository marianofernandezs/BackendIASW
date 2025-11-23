from typing import List, Optional, Dict

from Application.Interfaces.recipe_repository import IRecipeRepository
from Domain.Entities.recipe import Recipe
from Domain.Exceptions.custom_exceptions import RecipeNotFoundException

class InMemoryRecipeRepository(IRecipeRepository):
    """Implementación en memoria del repositorio de recetas."""

    def __init__(self, initial_recipes: Optional[List[Recipe]] = None):
        self._recipes: Dict[str, Recipe] = {}
        if initial_recipes:
            for recipe in initial_recipes:
                self._recipes[recipe.id] = recipe

    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Obtiene una receta por su ID."""
        return self._recipes.get(recipe_id)

    def get_all(self) -> List[Recipe]:
        """Obtiene todas las recetas."""
        return list(self._recipes.values())

    def add_recipe(self, recipe: Recipe) -> None:
        """Añade una nueva receta al repositorio."""
        if recipe.id in self._recipes:
            print(f"Advertencia: Receta con ID {recipe.id} ya existe. Sobrescribiendo.")
        self._recipes[recipe.id] = recipe

