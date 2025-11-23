from dataclasses import dataclass
from typing import Optional
from Assets.Scripts.domain.enums import OrderStatus

@dataclass(frozen=True)
class OrderLocationDTO:
    """
    DTO para transferir datos de ubicación de un pedido al cliente.
    """
    order_id: str
    latitude: float
    longitude: float
    status: OrderStatus

@dataclass(frozen=True)
class UpdateLocationCommand:
    """
    DTO para la entrada de la acción de actualización de ubicación del repartidor.
    """
    delivery_person_id: str
    latitude: float
    longitude: float

@dataclass(frozen=True)
class MarkOrderDeliveredCommand:
    """
    DTO para la entrada de la acción de marcar un pedido como entregado.
    """
    order_id: str

@dataclass(frozen=True)
class AssignDeliveryPersonCommand:
    """
    DTO para la entrada de la acción de asignar un repartidor a un pedido.
    """
    order_id: str
    delivery_person_id: str
