from typing import List, Optional, Dict
import math

from Application.Interfaces.product_repository import IProductRepository
from Domain.Entities.product import Product
from Domain.Entities.pagination import PagingInfo, PaginatedResult
from Domain.Exceptions.custom_exceptions import ProductNotFoundException

class InMemoryProductRepository(IProductRepository):
    """Implementación en memoria del repositorio de productos."""

    def __init__(self, initial_products: Optional[List[Product]] = None):
        self._products: Dict[str, Product] = {}
        if initial_products:
            for product in initial_products:
                self._products[product.id] = product

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto por su ID."""
        return self._products.get(product_id)

    def get_paginated(
        self,
        page: int,
        page_size: int,
        search_term: Optional[str] = None,
        category_id: Optional[str] = None
    ) -> PaginatedResult[Product]:
        """Obtiene una lista paginada de productos, con opciones de búsqueda y filtrado."""
        filtered_products = list(self._products.values())

        # Aplicar filtro por categoría
        if category_id:
            filtered_products = [p for p in filtered_products if p.category_id == category_id]

        # Aplicar filtro por término de búsqueda (insensible a mayúsculas/minúsculas)
        if search_term:
            search_term_lower = search_term.lower()
            filtered_products = [
                p for p in filtered_products
                if search_term_lower in p.name.lower() or search_term_lower in p.description.lower()
            ]

        # Ordenar (por nombre o relevancia, aquí por nombre para simplificar)
        filtered_products.sort(key=lambda p: p.name)

        total_items = len(filtered_products)
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
        current_page = max(1, min(page, total_pages)) # Asegurar que la página esté dentro de los límites

        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        paginated_items = filtered_products[start_index:end_index]

        paging_info = PagingInfo(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )
        return PaginatedResult(items=paginated_items, paging_info=paging_info)

    def update_product_stock(self, product_id: str, new_stock: int) -> None:
        """Actualiza el stock de un producto específico."""
        product = self._products.get(product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        product.stock = new_stock

    def add_product(self, product: Product) -> None:
        """Añade un nuevo producto al repositorio."""
        if product.id in self._products:
            # Podríamos lanzar una excepción o actualizar, dependiendo de la política
            print(f"Advertencia: Producto con ID {product.id} ya existe. Sobrescribiendo.")
        self._products[product.id] = product

    def get_all_products(self) -> List[Product]:
        """Obtiene todos los productos."""
        return list(self._products.values())

