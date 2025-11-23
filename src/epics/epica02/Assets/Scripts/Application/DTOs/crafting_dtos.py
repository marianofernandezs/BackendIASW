from dataclasses import dataclass

@dataclass
class CraftItemRequest:
    """DTO para la entrada del caso de uso de crafteo."""
    recipe_id: str
    quantity: int = 1

    def __post_init__(self):
        """Validación de cantidad."""
        if self.quantity <= 0:
            raise ValueError("La cantidad a craftear debe ser positiva.")

@dataclass
class CraftItemResponse:
    """DTO para la salida del caso de uso de crafteo."""
    crafted_product_id: str
    crafted_quantity: int
    success: bool
    message: str

