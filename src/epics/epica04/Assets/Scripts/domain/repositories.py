from abc import ABC, abstractmethod
from typing import Optional
from Assets.Scripts.domain.entities import Order, DeliveryPerson
from Assets.Scripts.domain.value_objects import Location

class IOrderRepository(ABC):
    """
    Contrato (interfaz) para el repositorio de Pedidos.
    Define las operaciones de persistencia para la entidad Order.
    """
    @abstractmethod
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Obtiene un pedido por su ID."""
        pass

    @abstractmethod
    def update_order(self, order: Order) -> None:
        """Actualiza un pedido existente."""
        pass

class IDeliveryPersonRepository(ABC):
    """
    Contrato (interfaz) para el repositorio de Repartidores.
    Define las operaciones de persistencia para la entidad DeliveryPerson.
    """
    @abstractmethod
    def get_delivery_person_by_id(self, delivery_person_id: str) -> Optional[DeliveryPerson]:
        """Obtiene un repartidor por su ID."""
        pass

    @abstractmethod
    def update_delivery_person(self, delivery_person: DeliveryPerson) -> None:
        """Actualiza un repartidor existente."""
        pass
