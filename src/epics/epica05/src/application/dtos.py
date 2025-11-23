from dataclasses import dataclass

@dataclass(frozen=True)
class CalificarPedidoRequest:
    """
    DTO (Data Transfer Object) para la entrada del caso de uso Calificar Pedido.
    Contiene los datos necesarios para que un cliente califique un pedido.
    """
    id_pedido: str
    id_cliente: str
    estrellas: int | None = None  # None si se omite la calificación
    comentarios: str | None = None

@dataclass(frozen=True)
class CalificarPedidoResponse:
    """
    DTO (Data Transfer Object) para la salida del caso de uso Calificar Pedido.
    Indica si la operación fue exitosa y su resultado.
    """
    exito: bool
    mensaje: str
    id_pedido: str
    estado_calificacion: str # CALIFICADO, OMITIDO, ERROR

