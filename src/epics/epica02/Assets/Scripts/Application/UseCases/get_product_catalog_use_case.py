from typing import List

from Application.Interfaces.product_repository import IProductRepository
from Application.Interfaces.category_repository import ICategoryRepository
from Application.DTOs.catalog_dtos import GetCatalogRequest, GetCatalogResponse
from Domain.Entities.pagination import PaginatedResult

class GetProductCatalogUseCase:
    """Caso de Uso: Obtener Catálogo de Productos Paginado y Filtrado."""

    def __init__(self, product_repo: IProductRepository, category_repo: ICategoryRepository):
        self._product_repo = product_repo
        self._category_repo = category_repo

    def execute(self, request: GetCatalogRequest) -> GetCatalogResponse:
        """
        Ejecuta el caso de uso para obtener el catálogo de productos.
        Incluye paginación, búsqueda y filtrado por categoría.
        """
        paginated_products = self._product_repo.get_paginated(
            page=request.page,
            page_size=request.page_size,
            search_term=request.search_term,
            category_id=request.category_id
        )

        # Obtener nombres de categorías para los DTOs
        all_categories = self._category_repo.get_all()
        category_names = {c.id: c.name for c in all_categories}

        return GetCatalogResponse.from_paginated_result(paginated_products, category_names)

