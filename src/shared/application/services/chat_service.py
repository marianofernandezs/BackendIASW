from typing import Optional

from domain.entities import ChatSession, Message, MessageSender, User
from application.use_cases.chat_use_cases import StartChatUseCase, SendMessageUseCase, HandleAgentResponseUseCase

class ChatService:
    """
    Servicio de aplicación para orquestar las operaciones de chat.
    Actúa como fachada para los casos de uso relacionados con el chat.
    """
    def __init__(self,
                 start_chat_use_case: StartChatUseCase,
                 send_message_use_case: SendMessageUseCase,
                 handle_agent_response_use_case: HandleAgentResponseUseCase):
        self._start_chat_uc = start_chat_use_case
        self._send_message_uc = send_message_use_case
        self._handle_agent_response_uc = handle_agent_response_use_case

    def start_chat_session(self, user_id: str) -> ChatSession:
        """Inicia una nueva sesión de chat o devuelve una existente para el usuario."""
        return self._start_chat_uc.execute(user_id)

    def send_user_message(self, session_id: str, content: str) -> Message:
        """Envía un mensaje de usuario a una sesión de chat y espera la respuesta del agente/bot."""
        user_message = self._send_message_uc.execute(session_id, MessageSender.USER, content)
        # Después de que el usuario envía un mensaje, el sistema debería generar una respuesta
        self._handle_agent_response_uc.execute(session_id, content)
        return user_message

    def get_chat_history(self, session: ChatSession) -> list[Message]:
        """Devuelve el historial de mensajes de una sesión."""
        # En una aplicación real, esto podría recargar la sesión desde el repositorio
        # Para este ejemplo, la sesión ya contendrá los mensajes.
        return session.messages
