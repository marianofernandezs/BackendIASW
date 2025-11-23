import abc
from src.domain.entities.calificacion import CalificacionPedido

class ICalificacionRepository(abc.ABC):
    """
    Interfaz abstracta para el repositorio de Calificaciones de Pedido.
    Define las operaciones para guardar calificaciones, desacoplando la
    lógica de negocio de los detalles de persistencia.
    """
    @abc.abstractmethod
    def guardar_calificacion(self, calificacion: CalificacionPedido) -> None:
        """Guarda una nueva calificación de pedido."""
        pass

