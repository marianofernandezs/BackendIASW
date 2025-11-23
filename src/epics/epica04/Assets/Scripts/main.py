import time
from Assets.Scripts.config import AppSettings
from Assets.Scripts.domain.entities import Order, DeliveryPerson
from Assets.Scripts.domain.enums import OrderStatus
from Assets.Scripts.domain.value_objects import Location
from Assets.Scripts.domain.repositories import IOrderRepository, IDeliveryPersonRepository
from Assets.Scripts.domain.use_cases import (
    TrackOrderLocationUseCase,
    UpdateDeliveryPersonLocationUseCase,
    MarkOrderAsDeliveredUseCase,
    AssignDeliveryPersonToOrderUseCase
)
from Assets.Scripts.application.dtos import (
    UpdateLocationCommand,
    MarkOrderDeliveredCommand,
    AssignDeliveryPersonCommand
)
from Assets.Scripts.application.services import OrderTrackingService, DeliveryManagementService
from Assets.Scripts.infrastructure.in_memory_repositories import (
    InMemoryOrderRepository,
    InMemoryDeliveryPersonRepository
)
from Assets.Scripts.infrastructure.gps_adapter import MockGPSAdapter

def setup_dependencies(settings: AppSettings) -> tuple[OrderTrackingService, DeliveryManagementService, MockGPSAdapter]:
    """
    Configura e inyecta las dependencias de la aplicación.
    Este es el punto donde se decide qué implementaciones de repositorios, etc., usar.
    """
    # Infraestructura
    order_repo: IOrderRepository = InMemoryOrderRepository()
    delivery_person_repo: IDeliveryPersonRepository = InMemoryDeliveryPersonRepository()
    
    # Inicializar con datos de prueba
    initial_location = Location(settings.DEFAULT_INITIAL_LATITUDE, settings.DEFAULT_INITIAL_LONGITUDE)
    repartidor_1 = DeliveryPerson(id="dp001", name="Juan Perez", current_location=initial_location)
    pedido_1 = Order(id="order123", customer_id="cust001", delivery_person_id="dp001", status=OrderStatus.IN_ROUTE)
    
    delivery_person_repo.update_delivery_person(repartidor_1)
    order_repo.update_order(pedido_1)

    # Use Cases
    track_order_location_uc = TrackOrderLocationUseCase(order_repo, delivery_person_repo)
    update_delivery_person_location_uc = UpdateDeliveryPersonLocationUseCase(delivery_person_repo)
    mark_order_as_delivered_uc = MarkOrderAsDeliveredUseCase(order_repo)
    assign_delivery_person_uc = AssignDeliveryPersonToOrderUseCase(order_repo)

    # Application Services
    order_tracking_service = OrderTrackingService(
        track_order_location_uc,
        mark_order_as_delivered_uc,
        assign_delivery_person_uc
    )
    delivery_management_service = DeliveryManagementService(update_delivery_person_location_uc)

    # Adaptador GPS (simulado)
    gps_adapter = MockGPSAdapter(initial_location)

    return order_tracking_service, delivery_management_service, gps_adapter

def simulate_customer_tracking(order_tracking_service: OrderTrackingService, order_id: str, iterations: int):
    """
    Simula la experiencia del cliente consultando el seguimiento del pedido.
    """
    print(f"\n--- Simulación: Cliente rastreando pedido {order_id} ---")
    for i in range(iterations):
        dto = order_tracking_service.get_order_real_time_location(order_id)
        if dto:
            print(f"[{i+1}/{iterations}] Pedido {dto.order_id}: Estado={dto.status.value}, "
                  f"Ubicación=({dto.latitude:.4f}, {dto.longitude:.4f})")
        else:
            print(f"[{i+1}/{iterations}] Pedido {order_id}: No se pudo obtener la ubicación o no existe.")
        time.sleep(1) # Simula un tiempo de espera entre consultas

def simulate_delivery_person_updates(delivery_management_service: DeliveryManagementService, 
                                     gps_adapter: MockGPSAdapter, 
                                     delivery_person_id: str, 
                                     iterations: int,
                                     update_interval: int):
    """
    Simula al repartidor actualizando su ubicación.
    """
    print(f"\n--- Simulación: Repartidor {delivery_person_id} actualizando ubicación ---")
    for i in range(iterations):
        new_location = gps_adapter.get_current_location()
        command = UpdateLocationCommand(
            delivery_person_id=delivery_person_id,
            latitude=new_location.latitude,
            longitude=new_location.longitude
        )
        success = delivery_management_service.update_delivery_person_location(command)
        if success:
            print(f"[{i+1}/{iterations}] Repartidor {delivery_person_id} actualizó a ({new_location.latitude:.4f}, {new_location.longitude:.4f})")
        else:
            print(f"[{i+1}/{iterations}] Repartidor {delivery_person_id} falló al actualizar.")
        time.sleep(update_interval) # Respeta el intervalo de actualización del GPS

def main():
    settings = AppSettings()
    order_tracking_service, delivery_management_service, gps_adapter = setup_dependencies(settings)

    order_id = "order123"
    delivery_person_id = "dp001"

    print("--- INICIO DE SIMULACIÓN DE SEGUIMIENTO DE PEDIDOS ---")
    print(f"Pedido inicial: {order_tracking_service.get_order_real_time_location(order_id)}")
    
    # Escenario 1: Repartidor actualiza su ubicación y cliente rastrea
    print("\nSimulación en curso: Repartidor actualiza y Cliente rastrea...")
    
    # Ejecutar en paralelo (para una app real, se usarían threads/async o servicios separados)
    # Aquí lo haremos secuencialmente para simplificar la demostración
    
    # 1. Repartidor actualiza su ubicación 3 veces
    simulate_delivery_person_updates(
        delivery_management_service, 
        gps_adapter, 
        delivery_person_id, 
        iterations=3, 
        update_interval=settings.GPS_UPDATE_INTERVAL_SECONDS // 3 # Para ver más actualizaciones en menos tiempo
    )

    # 2. Cliente rastrea 5 veces para ver las actualizaciones
    simulate_customer_tracking(order_tracking_service, order_id, iterations=5)

    # Escenario 2: Pedido entregado
    print(f"\n--- Escenario: Pedido {order_id} marcado como entregado ---")
    mark_delivered_command = MarkOrderDeliveredCommand(order_id=order_id)
    success = order_tracking_service.mark_order_delivered(mark_delivered_command)
    
    if success:
        print(f"Pedido {order_id} marcado como entregado con éxito.")
        # Cliente intenta rastrear de nuevo
        dto = order_tracking_service.get_order_real_time_location(order_id)
        if dto:
            print(f"Cliente ve: Pedido {dto.order_id}: Estado={dto.status.value}, "
                  f"Ubicación=({dto.latitude:.4f}, {dto.longitude:.4f}) (ubicación debería ser 0,0 si no está en ruta)")
        else:
            print(f"Cliente ve: Pedido {order_id}: No se pudo obtener la ubicación o no existe.")
    else:
        print(f"Fallo al marcar el pedido {order_id} como entregado.")

    print("\n--- FIN DE SIMULACIÓN ---")

if __name__ == "__main__":
    main()
