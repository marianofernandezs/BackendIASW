from dataclasses import dataclass, field
import datetime
import uuid

@dataclass(frozen=True) # Calificaciones son inmutables una vez creadas
class CalificacionPedido:
    """
    Representa una calificación específica para un pedido.
    Contiene el ID del pedido, el cliente, las estrellas, los comentarios y la fecha.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    id_pedido: str
    id_cliente: str
    estrellas: int
    comentarios: str | None
    fecha_calificacion: datetime.datetime = field(default_factory=datetime.datetime.now)

