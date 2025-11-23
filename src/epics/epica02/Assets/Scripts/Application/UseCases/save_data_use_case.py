from typing import Dict, Any

from Application.Interfaces.product_repository import IProductRepository
from Application.Interfaces.category_repository import ICategoryRepository
from Application.Interfaces.inventory_repository import IInventoryRepository
from Application.Interfaces.recipe_repository import IRecipeRepository
from Application.Interfaces.persistence_service import IPersistenceService

class SaveDataUseCase:
    """Caso de Uso: Persistir el estado actual de los datos del sistema."""

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
        inventory_repo: IInventoryRepository,
        recipe_repo: IRecipeRepository,
        persistence_service: IPersistenceService,
        persistence_file_path: str = "game_data.json"
    ):
        self._product_repo = product_repo
        self._category_repo = category_repo
        self._inventory_repo = inventory_repo
        self._recipe_repo = recipe_repo
        self._persistence_service = persistence_service
        self._persistence_file_path = persistence_file_path

    def execute(self) -> None:
        """
        Guarda todos los datos relevantes de los repositorios a través del servicio de persistencia.
        """
        data_to_save: Dict[str, Any] = {
            "products": [p.__dict__ for p in self._product_repo.get_all_products()],
            "categories": [c.__dict__ for c in self._category_repo.get_all()],
            "recipes": [self._recipe_to_dict(r) for r in self._recipe_repo.get_all()],
            "inventory": [item.__dict__ for item in self._inventory_repo.get_all_inventory_items().values()]
        }
        self._persistence_service.save_data(data_to_save, self._persistence_file_path)
        print(f"Datos guardados en '{self._persistence_file_path}'.")

    def _recipe_to_dict(self, recipe) -> Dict[str, Any]:
        """Convierte una entidad Recipe a un diccionario para serialización."""
        recipe_dict = recipe.__dict__.copy()
        recipe_dict["ingredients"] = [ing.__dict__ for ing in recipe.ingredients]
        return recipe_dict

