from abc import ABC, abstractmethod
from datetime import datetime

from domain.entities import MessageSender

class IAgentService(ABC):
    """Interfaz para interactuar con el sistema de agentes (humanos/bots)."""
    @abstractmethod
    def get_human_agent_response(self, user_message_content: str) -> str:
        """Simula la respuesta de un agente humano."""
        pass

    @abstractmethod
    def get_bot_response(self, user_message_content: str) -> str:
        """Simula la respuesta de un bot."""
        pass

    @abstractmethod
    def get_available_agent_id(self) -> str | None:
        """Devuelve un ID de agente humano disponible o None."""
        pass

class ITimeService(ABC):
    """Interfaz para abstraer el servicio de tiempo, útil para pruebas."""
    @abstractmethod
    def get_current_time(self) -> datetime:
        """Obtiene la hora actual del sistema."""
        pass
