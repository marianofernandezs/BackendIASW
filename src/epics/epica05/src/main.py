import datetime

from src.domain.entities.pedido import Pedido, EstadoEntrega, EstadoCalificacion
from src.domain.entities.calificacion import CalificacionPedido

from src.domain.use_cases.calificar_pedido_interactor import CalificarPedidoInteractor

from src.application.services.calificar_pedido_service import CalificarPedidoService

from src.infrastructure.repositories.in_memory_pedido_repository import InMemoryPedidoRepository
from src.infrastructure.repositories.in_memory_calificacion_repository import InMemoryCalificacionRepository
from src.infrastructure.config.rating_settings import RatingSettings

from src.presentation.controllers.rating_controller import RatingController

from src.shared.event_dispatcher import EventDispatcher
from src.shared.events import PedidoCalificadoEvent, CalificacionOmitidaEvent

# --- Handlers de Eventos de Ejemplo ---
def handle_pedido_calificado(event: PedidoCalificadoEvent):
    """Manejador de ejemplo para el evento PedidoCalificadoEvent."""
    print(f"\n[EVENTO] Pedido {event.id_pedido} CALIFICADO con {event.estrellas} estrellas. Comentarios: '{event.comentarios}'")
    # Aquí se podría enviar una notificación, actualizar un dashboard, etc.

def handle_calificacion_omitida(event: CalificacionOmitidaEvent):
    """Manejador de ejemplo para el evento CalificacionOmitidaEvent."""
    print(f"\n[EVENTO] Pedido {event.id_pedido} - Calificación OMITIDA.")
    # Aquí se podría registrar un log, enviar un recordatorio futuro, etc.

def setup_event_handlers():
    """Configura los manejadores de eventos."""
    EventDispatcher.register_handler(PedidoCalificadoEvent, handle_pedido_calificado)
    EventDispatcher.register_handler(CalificacionOmitidaEvent, handle_calificacion_omitida)

# --- Composición de dependencias (Composition Root) ---
def build_rating_system():
    """
    Construye y configura el sistema de calificación completo,
    inyectando las dependencias.
    """
    # 1. Configuración (simulando ScriptableObject)
    # Se podría cargar desde un archivo JSON:
    # rating_settings = RatingSettings.load_from_json("path/to/rating_config.json")
    rating_settings = RatingSettings(min_estrellas=1, max_estrellas=5)

    # 2. Repositorios de Infraestructura (implementaciones en memoria)
    pedido_repo = InMemoryPedidoRepository()
    calificacion_repo = InMemoryCalificacionRepository()

    # 3. Interactor de Caso de Uso de Dominio
    calificar_pedido_interactor = CalificarPedidoInteractor(
        pedido_repo=pedido_repo,
        calificacion_repo=calificacion_repo
    )

    # 4. Servicio de Aplicación
    calificar_pedido_service = CalificarPedidoService(
        interactor=calificar_pedido_interactor,
        settings=rating_settings
    )

    # 5. Controlador de Presentación
    rating_controller = RatingController(
        calificar_pedido_service=calificar_pedido_service
    )

    return pedido_repo, calificacion_repo, rating_controller

if __name__ == "__main__":
    print("Iniciando el sistema de calificación de pedidos...")

    # Registrar los manejadores de eventos al inicio
    setup_event_handlers()

    # Construir el sistema
    pedido_repo, calificacion_repo, rating_controller = build_rating_system()

    # --- Preparar datos iniciales (simulación de pedidos entregados) ---
    pedido1 = Pedido(id="PED-001", id_cliente="CLI-001", estado_entrega=EstadoEntrega.ENTREGADO)
    pedido2 = Pedido(id="PED-002", id_cliente="CLI-001", estado_entrega=EstadoEntrega.ENTREGADO)
    pedido3 = Pedido(id="PED-003", id_cliente="CLI-002", estado_entrega=EstadoEntrega.ENTREGADO)
    pedido_repo.guardar_pedido(pedido1)
    pedido_repo.guardar_pedido(pedido2)
    pedido_repo.guardar_pedido(pedido3)

    print("\n--- Estado inicial de pedidos ---")
    print(f"Pedido 1: {pedido_repo.obtener_pedido('PED-001').estado_calificacion.name}")
    print(f"Pedido 2: {pedido_repo.obtener_pedido('PED-002').estado_calificacion.name}")
    print(f"Pedido 3: {pedido_repo.obtener_pedido('PED-003').estado_calificacion.name}")

    # --- Escenario: Calificación exitosa (US-11) ---
    print("\n--- Ejecutando Escenario: Calificación exitosa (US-11) ---")
    # Cliente CLI-001 califica el PED-001 con 4 estrellas
    response1 = rating_controller.manejar_calificacion(
        id_pedido="PED-001",
        id_cliente="CLI-001",
        estrellas=4,
        comentarios="Entrega rápida y producto en buen estado."
    )
    print(f"Respuesta del controlador para PED-001: {response1.mensaje} (Exito: {response1.exito})")
    print(f"Estado del PED-001 después de calificar: {pedido_repo.obtener_pedido('PED-001').estado_calificacion.name}")
    print(f"Calificaciones guardadas para PED-001: {calificacion_repo.obtener_calificaciones_por_pedido('PED-001')}")

    # --- Escenario: Calificación omitida (US-11) ---
    print("\n--- Ejecutando Escenario: Calificación omitida (US-11) ---")
    # Cliente CLI-001 omite la calificación del PED-002
    response2 = rating_controller.manejar_calificacion(
        id_pedido="PED-002",
        id_cliente="CLI-001",
        estrellas=None,
        comentarios=None # Los comentarios son ignorados si estrellas es None
    )
    print(f"Respuesta del controlador para PED-002: {response2.mensaje} (Exito: {response2.exito})")
    print(f"Estado del PED-002 después de omitir: {pedido_repo.obtener_pedido('PED-002').estado_calificacion.name}")
    print(f"Calificaciones guardadas para PED-002: {calificacion_repo.obtener_calificaciones_por_pedido('PED-002')}")


    # --- Escenario: Intentar calificar un pedido ya calificado ---
    print("\n--- Ejecutando Escenario: Intentar calificar un pedido ya calificado ---")
    response_error_calificado = rating_controller.manejar_calificacion(
        id_pedido="PED-001",
        id_cliente="CLI-001",
        estrellas=5,
        comentarios="¡Realmente excelente!"
    )
    print(f"Respuesta del controlador para PED-001 (reintento): {response_error_calificado.mensaje} (Exito: {response_error_calificado.exito})")
    
    # --- Escenario: Intentar calificar un pedido con estrellas fuera de rango ---
    print("\n--- Ejecutando Escenario: Calificación con estrellas fuera de rango ---")
    response_error_rango = rating_controller.manejar_calificacion(
        id_pedido="PED-003",
        id_cliente="CLI-002",
        estrellas=6, # Fuera de rango 1-5
        comentarios="Demasiado bueno!"
    )
    print(f"Respuesta del controlador para PED-003 (fuera de rango): {response_error_rango.mensaje} (Exito: {response_error_rango.exito})")
    print(f"Estado del PED-003 después del error: {pedido_repo.obtener_pedido('PED-003').estado_calificacion.name}")

    # --- Escenario: Calificar pedido_3 correctamente ---
    print("\n--- Ejecutando Escenario: Calificar pedido_3 correctamente ---")
    response3 = rating_controller.manejar_calificacion(
        id_pedido="PED-003",
        id_cliente="CLI-002",
        estrellas=5,
        comentarios="Servicio excepcional, como siempre."
    )
    print(f"Respuesta del controlador para PED-003: {response3.mensaje} (Exito: {response3.exito})")
    print(f"Estado del PED-003 después de calificar: {pedido_repo.obtener_pedido('PED-003').estado_calificacion.name}")
    print(f"Calificaciones guardadas para PED-003: {calificacion_repo.obtener_calificaciones_por_pedido('PED-003')}")

    print("\nSistema de calificación finalizado.")

