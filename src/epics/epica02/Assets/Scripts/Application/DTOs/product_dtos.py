from dataclasses import dataclass
from typing import Optional

from Domain.Entities.product import Product

@dataclass
class ProductDto:
    """DTO para la visualización de detalles de un producto."""
    id: str
    name: str
    description: str
    price: float
    category_name: str
    stock: int
    is_available: bool

    @classmethod
    def from_entity(cls, product: Product, category_name: str) -> "ProductDto":
        """Crea un DTO a partir de una entidad Product y nombre de categoría."""
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category_name=category_name,
            stock=product.stock,
            is_available=product.is_available()
        )

