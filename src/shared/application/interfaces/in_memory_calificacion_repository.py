from typing import Dict, List
from src.domain.entities.calificacion import CalificacionPedido
from src.domain.use_cases.interfaces.calificacion_repository import ICalificacionRepository

class InMemoryCalificacionRepository(ICalificacionRepository):
    """
    Implementación en memoria del repositorio de Calificaciones de Pedido.
    Almacena las calificaciones en una lista en memoria.
    """
    _calificaciones: List[CalificacionPedido] = []

    def __init__(self, initial_data: Optional[List[CalificacionPedido]] = None):
        if initial_data:
            self._calificaciones.extend(initial_data)

    def guardar_calificacion(self, calificacion: CalificacionPedido) -> None:
        """Guarda una nueva calificación de pedido en la "base de datos" en memoria."""
        self._calificaciones.append(calificacion)
        print(f"DEBUG: Calificación guardada: {calificacion}")

    def obtener_calificaciones_por_pedido(self, id_pedido: str) -> List[CalificacionPedido]:
        """Obtiene todas las calificaciones para un pedido específico."""
        return [c for c in self._calificaciones if c.id_pedido == id_pedido]

    def reset(self):
        """Reinicia el repositorio para pruebas."""
        self._calificaciones = []

