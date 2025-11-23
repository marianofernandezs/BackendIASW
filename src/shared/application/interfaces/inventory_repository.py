from abc import ABC, abstractmethod
from typing import Optional, Dict

from Domain.Entities.inventory import InventoryItem

class IInventoryRepository(ABC):
    """Interfaz (ABC) para el repositorio de inventario."""

    @abstractmethod
    def get_item_quantity(self, product_id: str) -> int:
        """Obtiene la cantidad de un producto en el inventario."""
        pass

    @abstractmethod
    def update_item_quantity(self, product_id: str, new_quantity: int) -> None:
        """Actualiza la cantidad de un producto en el inventario."""
        pass

    @abstractmethod
    def add_item_quantity(self, product_id: str, quantity_to_add: int) -> None:
        """Añade una cantidad a un producto existente en el inventario."""
        pass

    @abstractmethod
    def remove_item_quantity(self, product_id: str, quantity_to_remove: int) -> None:
        """Remueve una cantidad de un producto del inventario."""
        pass

    @abstractmethod
    def get_all_inventory_items(self) -> Dict[str, InventoryItem]:
        """Obtiene todos los ítems del inventario."""
        pass

