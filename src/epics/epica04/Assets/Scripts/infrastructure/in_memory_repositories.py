from typing import Dict, Optional
from Assets.Scripts.domain.entities import Order, DeliveryPerson
from Assets.Scripts.domain.repositories import IOrderRepository, IDeliveryPersonRepository
from Assets.Scripts.domain.value_objects import Location
from Assets.Scripts.domain.enums import OrderStatus

class InMemoryOrderRepository(IOrderRepository):
    """
    Implementación en memoria del IOrderRepository.
    Útil para pruebas o desarrollo inicial.
    """
    def __init__(self, initial_orders: Optional[Dict[str, Order]] = None):
        self._orders: Dict[str, Order] = initial_orders if initial_orders is not None else {}

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Obtiene un pedido por su ID desde la memoria."""
        # Se devuelve una copia para evitar modificaciones externas directas a la entidad almacenada
        return self._orders.get(order_id)

    def update_order(self, order: Order) -> None:
        """Actualiza un pedido en memoria."""
        self._orders[order.id] = order

class InMemoryDeliveryPersonRepository(IDeliveryPersonRepository):
    """
    Implementación en memoria del IDeliveryPersonRepository.
    Útil para pruebas o desarrollo inicial.
    """
    def __init__(self, initial_delivery_persons: Optional[Dict[str, DeliveryPerson]] = None):
        self._delivery_persons: Dict[str, DeliveryPerson] = initial_delivery_persons if initial_delivery_persons is not None else {}

    def get_delivery_person_by_id(self, delivery_person_id: str) -> Optional[DeliveryPerson]:
        """Obtiene un repartidor por su ID desde la memoria."""
        return self._delivery_persons.get(delivery_person_id)

    def update_delivery_person(self, delivery_person: DeliveryPerson) -> None:
        """Actualiza un repartidor en memoria."""
        self._delivery_persons[delivery_person.id] = delivery_person
