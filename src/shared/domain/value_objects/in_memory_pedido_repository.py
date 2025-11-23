from typing import Dict, Optional
from src.domain.entities.pedido import Pedido, EstadoCalificacion
from src.domain.use_cases.interfaces.pedido_repository import IPedidoRepository

class InMemoryPedidoRepository(IPedidoRepository):
    """
    Implementación en memoria del repositorio de Pedidos.
    Ideal para pruebas o prototipos rápidos.
    Simula una base de datos con un diccionario.
    """
    _pedidos: Dict[str, Pedido] = {}

    def __init__(self, initial_data: Optional[Dict[str, Pedido]] = None):
        if initial_data:
            self._pedidos.update(initial_data)

    def obtener_pedido(self, id_pedido: str) -> Optional[Pedido]:
        """Obtiene un pedido por su ID de la "base de datos" en memoria."""
        return self._pedidos.get(id_pedido)

    def actualizar_pedido_estado(self, pedido: Pedido) -> None:
        """Actualiza el estado de un pedido existente en la "base de datos" en memoria."""
        if pedido.id not in self._pedidos:
            raise ValueError(f"El pedido con ID {pedido.id} no existe para actualizar.")
        self._pedidos[pedido.id] = pedido # Sobrescribe el pedido con la nueva versión

    def guardar_pedido(self, pedido: Pedido) -> None:
        """Guarda un nuevo pedido en la "base de datos" en memoria."""
        if pedido.id in self._pedidos:
            raise ValueError(f"El pedido con ID {pedido.id} ya existe.")
        self._pedidos[pedido.id] = pedido

    def reset(self):
        """Reinicia el repositorio para pruebas."""
        self._pedidos = {}

