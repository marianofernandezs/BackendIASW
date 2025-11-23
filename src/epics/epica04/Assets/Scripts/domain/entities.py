from dataclasses import dataclass
from typing import Optional
from Assets.Scripts.domain.value_objects import Location
from Assets.Scripts.domain.enums import OrderStatus

@dataclass
class Order:
    """
    Entidad que representa un pedido.
    """
    id: str
    customer_id: str
    delivery_person_id: Optional[str]
    status: OrderStatus

    def assign_delivery_person(self, delivery_person_id: str) -> None:
        """Asigna un repartidor al pedido."""
        self.delivery_person_id = delivery_person_id
        if self.status == OrderStatus.PENDING:
            self.status = OrderStatus.IN_ROUTE

    def mark_as_delivered(self) -> None:
        """Marca el pedido como entregado."""
        self.status = OrderStatus.DELIVERED

@dataclass
class DeliveryPerson:
    """
    Entidad que representa un repartidor.
    """
    id: str
    name: str
    current_location: Optional[Location] = None

    def update_location(self, new_location: Location) -> None:
        """Actualiza la ubicación actual del repartidor."""
        self.current_location = new_location
