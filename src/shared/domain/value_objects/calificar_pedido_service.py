from src.application.dtos import CalificarPedidoRequest, CalificarPedidoResponse
from src.domain.use_cases.calificar_pedido_interactor import CalificarPedidoInteractor
from src.infrastructure.config.rating_settings import RatingSettings

class CalificarPedidoService:
    """
    Servicio de aplicación para calificar un pedido.
    Actúa como fachada para el caso de uso `CalificarPedidoInteractor`,
    maneja DTOs y encapsula la configuración de calificación.
    """
    def __init__(self, interactor: CalificarPedidoInteractor, settings: RatingSettings):
        self.interactor = interactor
        self.settings = settings

    def ejecutar(self, request: CalificarPedidoRequest) -> CalificarPedidoResponse:
        """
        Ejecuta el proceso de calificación de un pedido.
        """
        try:
            self.interactor.ejecutar(
                id_pedido=request.id_pedido,
                id_cliente=request.id_cliente,
                estrellas=request.estrellas,
                comentarios=request.comentarios,
                min_estrellas=self.settings.min_estrellas,
                max_estrellas=self.settings.max_estrellas
            )
            
            if request.estrellas is not None:
                return CalificarPedidoResponse(
                    exito=True,
                    mensaje="Pedido calificado exitosamente.",
                    id_pedido=request.id_pedido,
                    estado_calificacion="CALIFICADO"
                )
            else:
                return CalificarPedidoResponse(
                    exito=True,
                    mensaje="Calificación de pedido omitida.",
                    id_pedido=request.id_pedido,
                    estado_calificacion="OMITIDO"
                )
        except ValueError as e:
            return CalificarPedidoResponse(
                exito=False,
                mensaje=str(e),
                id_pedido=request.id_pedido,
                estado_calificacion="ERROR"
            )
        except Exception as e:
            # Captura cualquier otra excepción inesperada
            return CalificarPedidoResponse(
                exito=False,
                mensaje=f"Ocurrió un error inesperado: {str(e)}",
                id_pedido=request.id_pedido,
                estado_calificacion="ERROR"
            )

