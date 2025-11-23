from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from Domain.Entities.product import Product
from Domain.Entities.pagination import PagingInfo, PaginatedResult

class IProductRepository(ABC):
    """Interfaz (ABC) para el repositorio de productos."""

    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto por su ID."""
        pass

    @abstractmethod
    def get_paginated(
        self,
        page: int,
        page_size: int,
        search_term: Optional[str] = None,
        category_id: Optional[str] = None
    ) -> PaginatedResult[Product]:
        """Obtiene una lista paginada de productos, con opciones de búsqueda y filtrado."""
        pass

    @abstractmethod
    def update_product_stock(self, product_id: str, new_stock: int) -> None:
        """Actualiza el stock de un producto específico."""
        pass

    @abstractmethod
    def add_product(self, product: Product) -> None:
        """Añade un nuevo producto al repositorio."""
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        """Obtiene todos los productos."""
        pass

