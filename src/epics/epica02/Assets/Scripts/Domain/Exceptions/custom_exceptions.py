class DomainException(Exception):
    """Excepción base para errores de dominio."""
    pass

class ProductNotFoundException(DomainException):
    """Se lanza cuando un producto no se encuentra."""
    def __init__(self, product_id: str):
        super().__init__(f"Producto con ID '{product_id}' no encontrado.")
        self.product_id = product_id

class CategoryNotFoundException(DomainException):
    """Se lanza cuando una categoría no se encuentra."""
    def __init__(self, category_id: str):
        super().__init__(f"Categoría con ID '{category_id}' no encontrada.")
        self.category_id = category_id

class InsufficientStockException(DomainException):
    """Se lanza cuando no hay suficiente stock de un producto."""
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(f"Stock insuficiente para producto '{product_id}'. Solicitado: {requested}, Disponible: {available}.")
        self.product_id = product_id
        self.requested = requested
        self.available = available

class RecipeNotFoundException(DomainException):
    """Se lanza cuando una receta no se encuentra."""
    def __init__(self, recipe_id: str):
        super().__init__(f"Receta con ID '{recipe_id}' no encontrada.")
        self.recipe_id = recipe_id

class CraftingFailedException(DomainException):
    """Se lanza cuando el proceso de crafteo falla por razones genéricas."""
    def __init__(self, message: str = "El crafteo ha fallado."):
        super().__init__(message)

