from src.application.dtos import CalificarPedidoRequest, CalificarPedidoResponse
from src.application.services.calificar_pedido_service import CalificarPedidoService

class RatingController:
    """
    Controlador de la capa de presentación para la calificación de pedidos.
    Recibe las solicitudes del cliente (e.g., de una API REST o una interfaz CLI),
    las traduce a DTOs de Request, llama al servicio de aplicación y
    formatea la respuesta.
    """
    def __init__(self, calificar_pedido_service: CalificarPedidoService):
        self.calificar_pedido_service = calificar_pedido_service

    def manejar_calificacion(self, id_pedido: str, id_cliente: str, estrellas: int | None, comentarios: str | None = None) -> CalificarPedidoResponse:
        """
        Maneja la solicitud de un cliente para calificar o omitir un pedido.
        
        Args:
            id_pedido: El ID del pedido.
            id_cliente: El ID del cliente.
            estrellas: El puntaje de 1 a 5, o None para omitir.
            comentarios: Comentarios opcionales.

        Returns:
            CalificarPedidoResponse: El resultado de la operación.
        """
        request = CalificarPedidoRequest(
            id_pedido=id_pedido,
            id_cliente=id_cliente,
            estrellas=estrellas,
            comentarios=comentarios
        )
        response = self.calificar_pedido_service.ejecutar(request)
        return response

    def _ejemplo_interaccion_cli(self) -> None:
        """
        Método de ejemplo para demostrar cómo interactuaría un cliente
        desde una interfaz de línea de comandos o similar.
        """
        print("\n--- Simulación de interacción del cliente ---")
        
        # Simulación de un pedido entregado para calificar
        pedido_id = "pedido_123"
        cliente_id = "cliente_A"

        # Simular una calificación exitosa
        print(f"\nCliente {cliente_id} calificando pedido {pedido_id} con 4 estrellas y 'Buen servicio'.")
        response_calificado = self.manejar_calificacion(pedido_id, cliente_id, 4, "Buen servicio.")
        print(f"Resultado: {response_calificado.mensaje} (Estado: {response_calificado.estado_calificacion})")

        # Simular una calificación omitida (ejemplo para un pedido diferente)
        pedido_id_2 = "pedido_456"
        print(f"\nCliente {cliente_id} omite la calificación del pedido {pedido_id_2}.")
        response_omitido = self.manejar_calificacion(pedido_id_2, cliente_id, None)
        print(f"Resultado: {response_omitido.mensaje} (Estado: {response_omitido.estado_calificacion})")

        # Intentar calificar un pedido ya calificado
        print(f"\nCliente {cliente_id} intenta recalificar pedido {pedido_id}.")
        response_recalificar = self.manejar_calificacion(pedido_id, cliente_id, 5, "Excelente!")
        print(f"Resultado: {response_recalificar.mensaje} (Estado: {response_recalificar.estado_calificacion})")

