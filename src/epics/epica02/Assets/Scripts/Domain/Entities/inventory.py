from dataclasses import dataclass
from .product import Product

@dataclass
class InventoryItem:
    """Entidad de Dominio: Item de Inventario."""
    product_id: str
    quantity: int

    def __post_init__(self):
        """Validación post-inicialización."""
        if self.quantity < 0:
            raise ValueError("La cantidad de un item de inventario no puede ser negativa.")

