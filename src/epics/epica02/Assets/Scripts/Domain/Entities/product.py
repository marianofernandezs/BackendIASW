from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    """Entidad de Dominio: Producto."""
    id: str
    name: str
    description: str
    price: float
    category_id: str
    stock: int = 0  # Stock actual del producto

    def is_available(self, quantity: int = 1) -> bool:
        """Verifica si hay suficiente stock para una cantidad dada."""
        return self.stock >= quantity

    def increase_stock(self, quantity: int) -> None:
        """Incrementa el stock del producto."""
        if quantity < 0:
            raise ValueError("La cantidad a aumentar no puede ser negativa.")
        self.stock += quantity

    def decrease_stock(self, quantity: int) -> None:
        """Decrementa el stock del producto."""
        if quantity < 0:
            raise ValueError("La cantidad a disminuir no puede ser negativa.")
        if not self.is_available(quantity):
            raise ValueError(f"Stock insuficiente para {self.name}. Disponible: {self.stock}, Requerido: {quantity}.")
        self.stock -= quantity

