from typing import Optional
from Assets.Scripts.domain.use_cases import (
    TrackOrderLocationUseCase,
    UpdateDeliveryPersonLocationUseCase,
    MarkOrderAsDeliveredUseCase,
    AssignDeliveryPersonToOrderUseCase
)
from Assets.Scripts.domain.value_objects import Location
from Assets.Scripts.application.dtos import (
    OrderLocationDTO,
    UpdateLocationCommand,
    MarkOrderDeliveredCommand,
    AssignDeliveryPersonCommand
)

class OrderTrackingService:
    """
    Servicio de aplicación para la gestión y seguimiento de pedidos.
    Actúa como fachada para los casos de uso relacionados con el pedido.
    """
    def __init__(self,
                 track_order_location_use_case: TrackOrderLocationUseCase,
                 mark_order_as_delivered_use_case: MarkOrderAsDeliveredUseCase,
                 assign_delivery_person_use_case: AssignDeliveryPersonToOrderUseCase):
        self._track_order_location_use_case = track_order_location_use_case
        self._mark_order_as_delivered_use_case = mark_order_as_delivered_use_case
        self._assign_delivery_person_use_case = assign_delivery_person_use_case

    def get_order_real_time_location(self, order_id: str) -> Optional[OrderLocationDTO]:
        """
        Obtiene la ubicación en tiempo real de un pedido para un cliente.
        """
        location, status = self._track_order_location_use_case.execute(order_id)
        if location and status:
            return OrderLocationDTO(
                order_id=order_id,
                latitude=location.latitude,
                longitude=location.longitude,
                status=status
            )
        return None

    def mark_order_delivered(self, command: MarkOrderDeliveredCommand) -> bool:
        """
        Marca un pedido como entregado.
        """
        return self._mark_order_as_delivered_use_case.execute(command.order_id)

    def assign_delivery_person(self, command: AssignDeliveryPersonCommand) -> bool:
        """
        Asigna un repartidor a un pedido.
        """
        return self._assign_delivery_person_use_case.execute(command.order_id, command.delivery_person_id)

class DeliveryManagementService:
    """
    Servicio de aplicación para la gestión de repartidores.
    Actúa como fachada para los casos de uso relacionados con el repartidor.
    """
    def __init__(self, update_delivery_person_location_use_case: UpdateDeliveryPersonLocationUseCase):
        self._update_delivery_person_location_use_case = update_delivery_person_location_use_case

    def update_delivery_person_location(self, command: UpdateLocationCommand) -> bool:
        """
        Actualiza la ubicación de un repartidor.
        """
        new_location = Location(command.latitude, command.longitude)
        return self._update_delivery_person_location_use_case.execute(command.delivery_person_id, new_location)
