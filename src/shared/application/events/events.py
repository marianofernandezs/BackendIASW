from dataclasses import dataclass
from src.shared.event_dispatcher import Event

@dataclass(frozen=True)
class PedidoCalificadoEvent(Event):
    """Evento emitido cuando un pedido es calificado exitosamente."""
    id_pedido: str
    estrellas: int
    comentarios: str | None

@dataclass(frozen=True)
class CalificacionOmitidaEvent(Event):
    """Evento emitido cuando un pedido no es calificado (se omite)."""
    id_pedido: str

