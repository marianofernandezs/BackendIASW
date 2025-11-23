import abc
from typing import Callable, Any, Dict

class Event:
    """Clase base para todos los eventos del sistema."""
    pass

class EventDispatcher:
    """
    Despachador de eventos simple para desacoplar la emisión de eventos de su manejo.
    Permite registrar múltiples manejadores para el mismo tipo de evento.
    """
    _handlers: Dict[type[Event], list[Callable[[Event], None]]] = {}

    @classmethod
    def register_handler(cls, event_type: type[Event], handler: Callable[[Event], None]) -> None:
        """Registra un manejador para un tipo de evento específico."""
        cls._handlers.setdefault(event_type, []).append(handler)
        print(f"DEBUG: Handler registrado para {event_type.__name__}")

    @classmethod
    def dispatch(cls, event: Event) -> None:
        """Despacha un evento a todos sus manejadores registrados."""
        event_type = type(event)
        if event_type in cls._handlers:
            for handler in cls._handlers[event_type]:
                print(f"DEBUG: Despachando evento {event_type.__name__} a handler {handler.__name__}")
                handler(event)
        else:
            print(f"DEBUG: No hay manejadores registrados para el evento {event_type.__name__}")

