from Application.Interfaces.product_repository import IProductRepository
from Application.Interfaces.category_repository import ICategoryRepository
from Application.DTOs.product_dtos import ProductDto
from Domain.Exceptions.custom_exceptions import ProductNotFoundException, CategoryNotFoundException

class GetProductDetailsUseCase:
    """Caso de Uso: Obtener Detalles de un Producto Específico."""

    def __init__(self, product_repo: IProductRepository, category_repo: ICategoryRepository):
        self._product_repo = product_repo
        self._category_repo = category_repo

    def execute(self, product_id: str) -> ProductDto:
        """
        Ejecuta el caso de uso para obtener los detalles de un producto.
        Lanza ProductNotFoundException si el producto no existe.
        """
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)

        category = self._category_repo.get_by_id(product.category_id)
        category_name = category.name if category else "Desconocida"

        return ProductDto.from_entity(product, category_name)

