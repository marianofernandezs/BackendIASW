from dataclasses import dataclass, field
from enum import Enum, auto
import uuid

class EstadoEntrega(Enum):
    """Enum para el estado de la entrega del pedido."""
    PENDIENTE = auto()
    ENTREGADO = auto()
    CANCELADO = auto()

class EstadoCalificacion(Enum):
    """Enum para el estado de la calificación del pedido."""
    PENDIENTE = auto()
    CALIFICADO = auto()
    OMITIDO = auto()

@dataclass
class Pedido:
    """
    Representa un pedido en el sistema.
    Contiene información básica del pedido y su estado de entrega/calificación.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    id_cliente: str
    estado_entrega: EstadoEntrega = EstadoEntrega.PENDIENTE
    estado_calificacion: EstadoCalificacion = EstadoCalificacion.PENDIENTE
    calificacion_estrellas: int | None = None
    comentarios_calificacion: str | None = None

    def marcar_entregado(self) -> None:
        """Marca el pedido como entregado."""
        if self.estado_entrega == EstadoEntrega.PENDIENTE:
            self.estado_entrega = EstadoEntrega.ENTREGADO
        else:
            raise ValueError("El pedido no puede ser marcado como entregado desde su estado actual.")

    def marcar_calificado(self, estrellas: int, comentarios: str | None) -> None:
        """
        Marca el pedido como calificado y guarda las estrellas y comentarios.
        """
        if self.estado_calificacion == EstadoCalificacion.PENDIENTE:
            self.estado_calificacion = EstadoCalificacion.CALIFICADO
            self.calificacion_estrellas = estrellas
            self.comentarios_calificacion = comentarios
        else:
            raise ValueError("El pedido ya ha sido calificado u omitido.")

    def marcar_calificacion_omitida(self) -> None:
        """Marca el pedido como calificación omitida."""
        if self.estado_calificacion == EstadoCalificacion.PENDIENTE:
            self.estado_calificacion = EstadoCalificacion.OMITIDO
        else:
            raise ValueError("El pedido ya ha sido calificado u omitido.")

