from dataclasses import dataclass, field
from typing import List
from .product import Product

@dataclass
class RecipeIngredient:
    """Entidad de Dominio: Ingrediente de Receta."""
    product_id: str
    quantity: int

    def __post_init__(self):
        """Validación post-inicialización."""
        if self.quantity <= 0:
            raise ValueError("La cantidad de un ingrediente debe ser positiva.")

@dataclass
class Recipe:
    """Entidad de Dominio: Receta."""
    id: str
    name: str
    output_product_id: str
    output_quantity: int
    ingredients: List[RecipeIngredient] = field(default_factory=list)

    def __post_init__(self):
        """Validación post-inicialización."""
        if self.output_quantity <= 0:
            raise ValueError("La cantidad de salida de la receta debe ser positiva.")
        if not self.ingredients:
            raise ValueError("Una receta debe tener al menos un ingrediente.")

