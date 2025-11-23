import abc
from typing import Optional
from src.domain.entities.pedido import Pedido, EstadoEntrega, EstadoCalificacion

class IPedidoRepository(abc.ABC):
    """
    Interfaz abstracta para el repositorio de Pedidos.
    Define las operaciones que deben ser implementadas por cualquier
    repositorio de pedidos concreto, desacoplando la lógica de negocio
    de los detalles de persistencia.
    """
    @abc.abstractmethod
    def obtener_pedido(self, id_pedido: str) -> Optional[Pedido]:
        """Obtiene un pedido por su ID."""
        pass

    @abc.abstractmethod
    def actualizar_pedido_estado(self, pedido: Pedido) -> None:
        """Actualiza el estado de un pedido existente."""
        pass
    
    @abc.abstractmethod
    def guardar_pedido(self, pedido: Pedido) -> None:
        """Guarda un nuevo pedido."""
        pass

