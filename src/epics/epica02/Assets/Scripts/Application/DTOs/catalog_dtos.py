from dataclasses import dataclass
from typing import List, Optional

from Domain.Entities.product import Product
from Domain.Entities.pagination import PaginatedResult, PagingInfo

@dataclass
class CatalogItemDto:
    """DTO para un elemento individual en el listado del catálogo."""
    id: str
    name: str
    price: float
    category_name: str
    is_available: bool

    @classmethod
    def from_entity(cls, product: Product, category_name: str) -> "CatalogItemDto":
        """Crea un DTO a partir de una entidad Product y nombre de categoría."""
        return cls(
            id=product.id,
            name=product.name,
            price=product.price,
            category_name=category_name,
            is_available=product.is_available()
        )

@dataclass
class GetCatalogRequest:
    """DTO para los parámetros de entrada del caso de uso de catálogo."""
    page: int = 1
    page_size: int = 12
    search_term: Optional[str] = None
    category_id: Optional[str] = None

    def __post_init__(self):
        """Validación de parámetros."""
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 12 # Valor por defecto

@dataclass
class GetCatalogResponse:
    """DTO para la respuesta del caso de uso de catálogo."""
    items: List[CatalogItemDto]
    paging_info: PagingInfo

    @classmethod
    def from_paginated_result(cls, paginated_products: PaginatedResult[Product], category_names: dict) -> "GetCatalogResponse":
        """Crea una respuesta DTO a partir de un resultado paginado de productos."""
        catalog_items = [
            CatalogItemDto.from_entity(p, category_names.get(p.category_id, "Desconocida"))
            for p in paginated_products.items
        ]
        return cls(
            items=catalog_items,
            paging_info=paginated_products.paging_info
        )

