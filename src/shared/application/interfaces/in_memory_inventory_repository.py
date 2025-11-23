from typing import Optional, Dict

from Application.Interfaces.inventory_repository import IInventoryRepository
from Domain.Entities.inventory import InventoryItem
from Domain.Exceptions.custom_exceptions import InsufficientStockException

class InMemoryInventoryRepository(IInventoryRepository):
    """Implementación en memoria del repositorio de inventario."""

    def __init__(self, initial_items: Optional[Dict[str, InventoryItem]] = None):
        # {product_id: InventoryItem}
        self._inventory_items: Dict[str, InventoryItem] = {}
        if initial_items:
            self._inventory_items.update(initial_items)

    def get_item_quantity(self, product_id: str) -> int:
        """Obtiene la cantidad de un producto en el inventario."""
        return self._inventory_items.get(product_id, InventoryItem(product_id=product_id, quantity=0)).quantity

    def update_item_quantity(self, product_id: str, new_quantity: int) -> None:
        """Actualiza la cantidad de un producto en el inventario."""
        if new_quantity < 0:
            raise ValueError("La cantidad en inventario no puede ser negativa.")
        if new_quantity == 0:
            if product_id in self._inventory_items:
                del self._inventory_items[product_id]
        else:
            self._inventory_items[product_id] = InventoryItem(product_id=product_id, quantity=new_quantity)

    def add_item_quantity(self, product_id: str, quantity_to_add: int) -> None:
        """Añade una cantidad a un producto existente en el inventario."""
        if quantity_to_add < 0:
            raise ValueError("La cantidad a añadir debe ser positiva.")
        current_quantity = self.get_item_quantity(product_id)
        self.update_item_quantity(product_id, current_quantity + quantity_to_add)

    def remove_item_quantity(self, product_id: str, quantity_to_remove: int) -> None:
        """Remueve una cantidad de un producto del inventario."""
        if quantity_to_remove < 0:
            raise ValueError("La cantidad a remover debe ser positiva.")
        current_quantity = self.get_item_quantity(product_id)
        if current_quantity < quantity_to_remove:
            raise InsufficientStockException(product_id, quantity_to_remove, current_quantity)
        self.update_item_quantity(product_id, current_quantity - quantity_to_remove)

    def get_all_inventory_items(self) -> Dict[str, InventoryItem]:
        """Obtiene todos los ítems del inventario."""
        return self._inventory_items

