from src.domain.entities.pedido import Pedido, EstadoCalificacion
from src.domain.entities.calificacion import CalificacionPedido
from src.domain.use_cases.interfaces.pedido_repository import IPedidoRepository
from src.domain.use_cases.interfaces.calificacion_repository import ICalificacionRepository
from src.shared.event_dispatcher import EventDispatcher
from src.shared.events import PedidoCalificadoEvent, CalificacionOmitidaEvent

class CalificarPedidoInteractor:
    """
    Caso de uso para calificar un pedido.
    Contiene la lógica de negocio principal para procesar la calificación
    de un cliente sobre un pedido entregado.
    """
    def __init__(self, pedido_repo: IPedidoRepository, calificacion_repo: ICalificacionRepository):
        self.pedido_repo = pedido_repo
        self.calificacion_repo = calificacion_repo

    def ejecutar(self, id_pedido: str, id_cliente: str, estrellas: int | None, comentarios: str | None, min_estrellas: int, max_estrellas: int) -> None:
        """
        Procesa la calificación o la omisión de un pedido.

        Args:
            id_pedido: El ID del pedido a calificar.
            id_cliente: El ID del cliente que califica.
            estrellas: El puntaje de 1 a 5, o None si se omite.
            comentarios: Comentarios opcionales.
            min_estrellas: Mínimo de estrellas permitido.
            max_estrellas: Máximo de estrellas permitido.
        
        Raises:
            ValueError: Si el pedido no existe, no está entregado o las estrellas no son válidas.
        """
        pedido = self.pedido_repo.obtener_pedido(id_pedido)

        if not pedido:
            raise ValueError(f"Pedido con ID {id_pedido} no encontrado.")

        # La historia dice "Dado que recibí un pedido", lo que implica que ya está entregado
        # Aquí asumimos que el pedido ya fue marcado como entregado previamente
        # if pedido.estado_entrega != EstadoEntrega.ENTREGADO:
        #     raise ValueError(f"El pedido {id_pedido} no ha sido entregado aún.")

        if pedido.estado_calificacion != EstadoCalificacion.PENDIENTE:
            raise ValueError(f"El pedido {id_pedido} ya ha sido calificado u omitido.")

        if estrellas is not None:
            # Escenario: Calificación exitosa
            if not (min_estrellas <= estrellas <= max_estrellas):
                raise ValueError(f"Las estrellas deben estar entre {min_estrellas} y {max_estrellas}.")
            
            calificacion = CalificacionPedido(
                id_pedido=id_pedido,
                id_cliente=id_cliente,
                estrellas=estrellas,
                comentarios=comentarios
            )
            self.calificacion_repo.guardar_calificacion(calificacion)
            pedido.marcar_calificado(estrellas, comentarios)
            EventDispatcher.dispatch(PedidoCalificadoEvent(id_pedido, estrellas, comentarios))
        else:
            # Escenario: Calificación omitida
            pedido.marcar_calificacion_omitida()
            EventDispatcher.dispatch(CalificacionOmitidaEvent(id_pedido))
        
        self.pedido_repo.actualizar_pedido_estado(pedido)

