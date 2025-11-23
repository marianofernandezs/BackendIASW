from typing import Optional
from dataclasses import dataclass

from domain.entities import ChatSession, Message, MessageSender, User, ChatSessionStatus
from application.interfaces.repositories import IMessageRepository, IUserRepository
from application.interfaces.services import ITimeService
from application.strategies.agent_response_strategy import IAgentResponseStrategy
from application.services.event_bus import EventBus

# --- Eventos ---
@dataclass
class ChatStarted:
    """Evento: Se inicia una nueva sesión de chat."""
    session_id: str
    user_id: str

@dataclass
class MessageReceived:
    """Evento: Se envía un mensaje a la sesión."""
    session_id: str
    message: Message

@dataclass
class AgentResponded:
    """Evento: Un agente (humano o bot) ha respondido."""
    session_id: str
    response_message: Message
    agent_type: str # 'HUMAN' o 'BOT'

@dataclass
class ChatEnded:
    """Evento: Una sesión de chat ha finalizado."""
    session_id: str

class StartChatUseCase:
    """Caso de uso para iniciar una nueva sesión de chat."""
    def __init__(self, message_repo: IMessageRepository, user_repo: IUserRepository, event_bus: EventBus):
        self._message_repo = message_repo
        self._user_repo = user_repo
        self._event_bus = event_bus

    def execute(self, user_id: str) -> ChatSession:
        """
        Inicia una nueva sesión de chat para el usuario dado.
        Si ya tiene una sesión activa, la devuelve.
        """
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado.")

        # Verificar si ya existe una sesión abierta para el usuario
        existing_session = self._message_repo.get_session_by_user_id(user_id)
        if existing_session and existing_session.status != ChatSessionStatus.CLOSED:
            print(f"DEBUG: Sesión activa encontrada para el usuario {user_id}.")
            return existing_session

        new_session = ChatSession(user_id=user_id)
        self._message_repo.save(new_session)
        self._event_bus.publish(ChatStarted(session_id=new_session.id, user_id=user_id))
        return new_session

class SendMessageUseCase:
    """Caso de uso para enviar un mensaje a una sesión de chat."""
    def __init__(self, message_repo: IMessageRepository, event_bus: EventBus):
        self._message_repo = message_repo
        self._event_bus = event_bus

    def execute(self, session_id: str, sender: MessageSender, content: str) -> Message:
        """Envía un mensaje a la sesión de chat especificada."""
        session = self._message_repo.get_by_id(session_id)
        if not session:
            raise ValueError(f"Sesión de chat con ID {session_id} no encontrada.")

        if session.status == ChatSessionStatus.CLOSED:
            raise ValueError("No se pueden enviar mensajes a una sesión de chat cerrada.")

        new_message = Message(session_id=session_id, sender=sender, content=content)
        session.add_message(new_message)
        self._message_repo.save(session) # Persiste la sesión con el nuevo mensaje
        self._event_bus.publish(MessageReceived(session_id=session_id, message=new_message))
        return new_message

class HandleAgentResponseUseCase:
    """Caso de uso para manejar la respuesta del agente (humano o bot)."""
    def __init__(self, message_repo: IMessageRepository, time_service: ITimeService,
                 agent_response_strategy: IAgentResponseStrategy, event_bus: EventBus):
        self._message_repo = message_repo
        self._time_service = time_service
        self._agent_response_strategy = agent_response_strategy
        self._event_bus = event_bus

    def execute(self, session_id: str, user_message_content: str) -> Optional[Message]:
        """
        Determina la estrategia de respuesta (humano/bot) y añade el mensaje de respuesta a la sesión.
        """
        session = self._message_repo.get_by_id(session_id)
        if not session:
            raise ValueError(f"Sesión de chat con ID {session_id} no encontrada.")

        response_message = self._agent_response_strategy.get_response(session, user_message_content)
        session.add_message(response_message)
        self._message_repo.save(session) # Persiste la sesión con el mensaje de respuesta

        agent_type_str = "AGENT" if response_message.sender == MessageSender.AGENT else "BOT"
        self._event_bus.publish(AgentResponded(session_id=session_id, response_message=response_message, agent_type=agent_type_str))
        return response_message
