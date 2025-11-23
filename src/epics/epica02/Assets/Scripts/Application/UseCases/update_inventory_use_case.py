from Application.Interfaces.inventory_repository import IInventoryRepository
from Application.Interfaces.product_repository import IProductRepository
from Domain.Exceptions.custom_exceptions import ProductNotFoundException

class UpdateInventoryUseCase:
    """Caso de Uso: Actualizar el Inventario de un Producto."""

    def __init__(self, inventory_repo: IInventoryRepository, product_repo: IProductRepository):
        self._inventory_repo = inventory_repo
        self._product_repo = product_repo

    def execute(self, product_id: str, quantity_change: int) -> None:
        """
        Ajusta la cantidad de un producto en el inventario.
        `quantity_change` puede ser positivo (añadir) o negativo (remover).
        Actualiza también el stock del producto en el repositorio de productos.
        """
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)

        if quantity_change > 0:
            self._inventory_repo.add_item_quantity(product_id, quantity_change)
            product.increase_stock(quantity_change)
        elif quantity_change < 0:
            self._inventory_repo.remove_item_quantity(product_id, abs(quantity_change))
            product.decrease_stock(abs(quantity_change)) # decrease_stock ya valida stock
        # Si quantity_change es 0, no hacer nada

        self._product_repo.update_product_stock(product_id, product.stock)

