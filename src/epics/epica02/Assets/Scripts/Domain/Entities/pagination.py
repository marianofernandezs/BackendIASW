from dataclasses import dataclass
from typing import List, TypeVar, Generic

T = TypeVar('T')

@dataclass
class PagingInfo:
    """Entidad de Dominio: Información de Paginación."""
    current_page: int
    page_size: int
    total_items: int
    total_pages: int

@dataclass
class PaginatedResult(Generic[T]):
    """Entidad de Dominio: Resultado Paginado."""
    items: List[T]
    paging_info: PagingInfo

