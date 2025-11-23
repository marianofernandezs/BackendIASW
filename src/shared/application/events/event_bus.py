from typing import Callable, Any, Dict

class EventBus:
    """Un sistema simple de publicación/suscripción para eventos."""
    def __init__(self):
        self._listeners: Dict[type, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: type, listener: Callable[[Any], None]):
        """Suscribe un listener a un tipo de evento específico."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: type, listener: Callable[[Any], None]):
        """Desuscribe un listener de un tipo de evento."""
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def publish(self, event: Any):
        """Publica un evento a todos los listeners suscritos."""
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(event)
