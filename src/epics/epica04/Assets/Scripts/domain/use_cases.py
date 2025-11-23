from typing import Optional
from Assets.Scripts.domain.entities import Order, DeliveryPerson
from Assets.Scripts.domain.enums import OrderStatus
from Assets.Scripts.domain.value_objects import Location
from Assets.Scripts.domain.repositories import IOrderRepository, IDeliveryPersonRepository

class TrackOrderLocationUseCase:
    """
    Caso de uso para el seguimiento de la ubicación de un pedido.
    Permite a un cliente ver dónde está su pedido.
    """
    def __init__(self, order_repo: IOrderRepository, delivery_person_repo: IDeliveryPersonRepository):
        self._order_repo = order_repo
        self._delivery_person_repo = delivery_person_repo

    def execute(self, order_id: str) -> Optional[tuple[Location, OrderStatus]]:
        """
        Ejecuta el caso de uso, devolviendo la ubicación del repartidor
        y el estado del pedido, si el pedido está en ruta.
        """
        order = self._order_repo.get_order_by_id(order_id)
        if not order:
            return None # Pedido no encontrado

        if order.status != OrderStatus.IN_ROUTE or not order.delivery_person_id:
            return Location(0.0, 0.0), order.status # No hay ubicación activa para mostrar

        delivery_person = self._delivery_person_repo.get_delivery_person_by_id(order.delivery_person_id)
        if delivery_person and delivery_person.current_location:
            return delivery_person.current_location, order.status
        
        return Location(0.0, 0.0), order.status # Repartidor o ubicación no encontrados, pero el pedido está en ruta

class UpdateDeliveryPersonLocationUseCase:
    """
    Caso de uso para actualizar la ubicación de un repartidor.
    Utilizado por la aplicación del repartidor.
    """
    def __init__(self, delivery_person_repo: IDeliveryPersonRepository):
        self._delivery_person_repo = delivery_person_repo

    def execute(self, delivery_person_id: str, new_location: Location) -> bool:
        """
        Actualiza la ubicación de un repartidor específico.
        Devuelve True si la actualización fue exitosa, False en caso contrario.
        """
        delivery_person = self._delivery_person_repo.get_delivery_person_by_id(delivery_person_id)
        if not delivery_person:
            return False # Repartidor no encontrado

        delivery_person.update_location(new_location)
        self._delivery_person_repo.update_delivery_person(delivery_person)
        return True

class MarkOrderAsDeliveredUseCase:
    """
    Caso de uso para marcar un pedido como entregado.
    Utilizado por la aplicación del repartidor al finalizar la entrega.
    """
    def __init__(self, order_repo: IOrderRepository):
        self._order_repo = order_repo

    def execute(self, order_id: str) -> bool:
        """
        Marca un pedido como entregado.
        Devuelve True si la operación fue exitosa, False en caso contrario.
        """
        order = self._order_repo.get_order_by_id(order_id)
        if not order:
            return False # Pedido no encontrado

        if order.status == OrderStatus.DELIVERED:
            return True # Ya estaba entregado
        
        order.mark_as_delivered()
        self._order_repo.update_order(order)
        return True

class AssignDeliveryPersonToOrderUseCase:
    """
    Caso de uso para asignar un repartidor a un pedido.
    """
    def __init__(self, order_repo: IOrderRepository):
        self._order_repo = order_repo

    def execute(self, order_id: str, delivery_person_id: str) -> bool:
        """
        Asigna un repartidor a un pedido.
        Devuelve True si la asignación fue exitosa, False en caso contrario.
        """
        order = self._order_repo.get_order_by_id(order_id)
        if not order:
            return False
        
        order.assign_delivery_person(delivery_person_id)
        self._order_repo.update_order(order)
        return True
