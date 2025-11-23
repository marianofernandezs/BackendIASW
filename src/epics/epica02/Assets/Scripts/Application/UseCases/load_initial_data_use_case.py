from typing import Dict, Any

from Application.Interfaces.product_repository import IProductRepository
from Application.Interfaces.category_repository import ICategoryRepository
from Application.Interfaces.inventory_repository import IInventoryRepository
from Application.Interfaces.recipe_repository import IRecipeRepository
from Application.Interfaces.persistence_service import IPersistenceService

from Infrastructure.Config.initial_data_config import InitialDataConfig

class LoadInitialDataUseCase:
    """
    Caso de Uso: Cargar datos iniciales en los repositorios
    si no hay datos persistidos, o cargar desde persistencia si existen.
    """

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
        inventory_repo: IInventoryRepository,
        recipe_repo: IRecipeRepository,
        persistence_service: IPersistenceService,
        initial_data_config: InitialDataConfig,
        persistence_file_path: str = "game_data.json"
    ):
        self._product_repo = product_repo
        self._category_repo = category_repo
        self._inventory_repo = inventory_repo
        self._recipe_repo = recipe_repo
        self._persistence_service = persistence_service
        self._initial_data_config = initial_data_config
        self._persistence_file_path = persistence_file_path

    def execute(self) -> None:
        """
        Carga datos: primero intenta desde persistencia, si no existe,
        carga desde la configuración inicial (ScriptableObject).
        """
        if self._persistence_service.data_exists(self._persistence_file_path):
            print(f"Cargando datos desde '{self._persistence_file_path}'...")
            persisted_data = self._persistence_service.load_data(self._persistence_file_path)
            self._load_from_persisted_data(persisted_data)
            print("Datos cargados correctamente.")
        else:
            print("No se encontraron datos persistidos. Cargando datos iniciales de configuración...")
            self._load_from_initial_config()
            print("Datos iniciales cargados. Por favor, guarde para persistirlos.")

    def _load_from_initial_config(self) -> None:
        """Carga datos desde el objeto de configuración inicial."""
        for category in self._initial_data_config.get_initial_categories():
            self._category_repo.add_category(category)
        for product in self._initial_data_config.get_initial_products():
            self._product_repo.add_product(product)
        for recipe in self._initial_data_config.get_initial_recipes():
            self._recipe_repo.add_recipe(recipe)
        for item in self._initial_data_config.get_initial_inventory():
            self._inventory_repo.add_item_quantity(item.product_id, item.quantity)

    def _load_from_persisted_data(self, data: Dict[str, Any]) -> None:
        """Carga datos desde un diccionario de datos persistidos."""
        # Limpiar repositorios actuales (si no están vacíos)
        # (Esto es específico de implementaciones en memoria; una DB real manejaría esto)

        # Cargar categorías
        for category_data in data.get("categories", []):
            self._category_repo.add_category(self._initial_data_config.category_from_dict(category_data))
        # Cargar productos
        for product_data in data.get("products", []):
            self._product_repo.add_product(self._initial_data_config.product_from_dict(product_data))
        # Cargar recetas
        for recipe_data in data.get("recipes", []):
            self._recipe_repo.add_recipe(self._initial_data_config.recipe_from_dict(recipe_data))
        # Cargar inventario
        for item_data in data.get("inventory", []):
            self._inventory_repo.add_item_quantity(item_data["product_id"], item_data["quantity"])

