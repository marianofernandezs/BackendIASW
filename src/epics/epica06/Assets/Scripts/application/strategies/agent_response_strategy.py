from abc import ABC, abstractmethod
from datetime import datetime

from domain.entities import ChatSession, Message, MessageSender, SupportAgent
from application.interfaces.services import IAgentService, ITimeService
from infrastructure.config.chat_config import SupportHoursConfig, ChatSettings

class IAgentResponseStrategy(ABC):
    """Interfaz abstracta para estrategias de respuesta de agentes."""
    @abstractmethod
    def get_response(self, session: ChatSession, user_message_content: str) -> Message:
        """Genera un mensaje de respuesta para la sesión."""
        pass

class HumanAgentResponseStrategy(IAgentResponseStrategy):
    """Estrategia para respuestas de agentes humanos."""
    def __init__(self, agent_service: IAgentService, time_service: ITimeService,
                 support_config: SupportHoursConfig, chat_settings: ChatSettings):
        self._agent_service = agent_service
        self._time_service = time_service
        self._support_config = support_config
        self._chat_settings = chat_settings

    def get_response(self, session: ChatSession, user_message_content: str) -> Message:
        """
        Determina si el horario de soporte es hábil. Si es así, busca un agente humano.
        Si no hay agente o fuera de horario, delega al bot.
        """
        current_time = self._time_service.get_current_time()
        is_business_hours = self._support_config.is_within_business_hours(current_time)

        if is_business_hours:
            agent_id = self._agent_service.get_available_agent_id()
            if agent_id:
                # Simular respuesta de agente humano
                response_content = self._agent_service.get_human_agent_response(user_message_content)
                session.agent_id = agent_id # Asigna el agente a la sesión
                return Message(sender=MessageSender.AGENT, content=response_content, session_id=session.id)

        # Si no hay agente disponible o fuera de horario, recurre al bot
        bot_strategy = BotResponseStrategy(self._agent_service, self._chat_settings)
        return bot_strategy.get_response(session, user_message_content)

class BotResponseStrategy(IAgentResponseStrategy):
    """Estrategia para respuestas de un bot."""
    def __init__(self, agent_service: IAgentService, chat_settings: ChatSettings):
        self._agent_service = agent_service
        self._chat_settings = chat_settings

    def get_response(self, session: ChatSession, user_message_content: str) -> Message:
        """Genera una respuesta automática del bot."""
        response_content = self._agent_service.get_bot_response(user_message_content)
        return Message(sender=MessageSender.BOT, content=response_content, session_id=session.id)
