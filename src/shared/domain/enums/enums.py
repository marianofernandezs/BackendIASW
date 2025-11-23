from enum import Enum

class OrderStatus(Enum):
    """
    Enumeración para los estados posibles de un pedido.
    """
    PENDING = "pendiente"
    IN_ROUTE = "en_ruta"
    DELIVERED = "entregado"
    CANCELLED = "cancelado"
