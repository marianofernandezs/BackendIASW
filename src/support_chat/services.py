"""
Módulo de servicios para la lógica de negocio de la aplicación support_chat.
Contiene clases para gestionar la disponibilidad, respuestas y persistencia de chat.
"""

from datetime import datetime, time
from django.utils import timezone # Importar timezone para manejar fechas conscientes de la zona horaria
from django.db import models
from support_chat.models import ChatSession, ChatMessage


class AgentAvailabilityService:
    """
    Determina si los agentes humanos están disponibles basándose en el horario de atención.
    """
    BUSINESS_START_HOUR = 9
    BUSINESS_END_HOUR = 18

    def is_agent_available(self, current_time: datetime) -> bool:
        """
        Verifica si la hora actual está dentro del horario de atención.
        :param current_time: Objeto datetime consciente de la zona horaria.
        :return: True si un agente está disponible, False en caso contrario.
        """
        # Asegurarse de que current_time sea consciente de la zona horaria
        if not timezone.is_aware(current_time):
            current_time = timezone.make_aware(current_time, timezone.get_current_timezone())

        start_time = current_time.replace(hour=self.BUSINESS_START_HOUR, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=self.BUSINESS_END_HOUR, minute=0, second=0, microsecond=0)

        return start_time <= current_time < end_time


class BotService:
    """
    Genera respuestas automáticas del bot.
    """
    def get_bot_response(self, message_content: str) -> str:
        """
        Devuelve una respuesta predefinida del bot.
        :param message_content: Contenido del mensaje del cliente (no usado por ahora).
        :return: Una cadena de texto con la respuesta del bot.
        """
        return "Hola, gracias por contactarnos. Nuestro horario de atención es de 9:00 a 18:00 hrs. " \
               "Un agente revisará tu consulta el próximo día hábil."


class AgentService:
    """
    Simula o proporciona respuestas de agentes humanos.
    """
    def get_agent_response(self, message_content: str) -> str:
        """
        Devuelve una respuesta simulada de un agente.
        :param message_content: Contenido del mensaje del cliente.
        :return: Una cadena de texto con la respuesta del agente.
        """
        return f"Gracias por tu mensaje, estamos revisando '{message_content}'. En breve te atenderá un agente."


class MessagePersistenceService:
    """
    Gestiona la persistencia de mensajes de chat en la base de datos.
    """
    def save_message(self, session: ChatSession, sender: str, content: str) -> ChatMessage:
        """
        Guarda un nuevo mensaje en la base de datos.
        :param session: La sesión de chat a la que pertenece el mensaje.
        :param sender: Quién envió el mensaje ('client', 'agent', 'bot').
        :param content: El contenido del mensaje.
        :return: El objeto ChatMessage creado.
        """
        return ChatMessage.objects.create(session=session, sender=sender, content=content)

    def get_messages_for_session(self, session: ChatSession) -> models.QuerySet:
        """
        Recupera todos los mensajes para una sesión de chat dada.
        :param session: La sesión de chat.
        :return: Un QuerySet de ChatMessage.
        """
        return session.messages.all().order_by('timestamp')


class ChatSessionService:
    """
    Gestiona el ciclo de vida de las sesiones de chat.
    """
    def create_session(self) -> ChatSession:
        """
        Crea una nueva sesión de chat con estado 'open'.
        :return: El objeto ChatSession recién creado.
        """
        return ChatSession.objects.create(status='open')

    def get_session(self, session_id: int) -> ChatSession:
        """
        Recupera una sesión de chat por su ID.
        :param session_id: El ID de la sesión.
        :return: El objeto ChatSession.
        :raises ChatSession.DoesNotExist: Si la sesión no existe.
        """
        return ChatSession.objects.get(id=session_id)


class ChatOrchestratorService:
    """
    Orquesta el flujo de chat, determinando la respuesta y persistiendo los mensajes.
    """
    def __init__(self,
                 agent_availability_service: AgentAvailabilityService,
                 bot_service: BotService,
                 agent_service: AgentService,
                 message_persistence_service: MessagePersistenceService,
                 chat_session_service: ChatSessionService):
        """
        Inicializa el orquestador con los servicios dependientes.
        """
        self._agent_availability_service = agent_availability_service
        self._bot_service = bot_service
        self._agent_service = agent_service
        self._message_persistence_service = message_persistence_service
        self._chat_session_service = chat_session_service

    def handle_incoming_message(self, session_id: int, client_message_content: str) -> ChatMessage:
        """
        Procesa un mensaje entrante del cliente, genera una respuesta y la persiste.
        :param session_id: El ID de la sesión de chat.
        :param client_message_content: Contenido del mensaje del cliente.
        :return: El objeto ChatMessage de la respuesta generada (bot o agente).
        """
        session = self._chat_session_service.get_session(session_id)

        # Persistir el mensaje del cliente
        self._message_persistence_service.save_message(session, 'client', client_message_content)

        # Determinar si el agente está disponible
        current_time = timezone.now()
        if self._agent_availability_service.is_agent_available(current_time):
            # Agente disponible, generar respuesta de agente
            response_content = self._agent_service.get_agent_response(client_message_content)
            response_sender = 'agent'
        else:
            # Agente no disponible, generar respuesta del bot
            response_content = self._bot_service.get_bot_response(client_message_content)
            response_sender = 'bot'

        # Persistir la respuesta generada
        response_message = self._message_persistence_service.save_message(
            session, response_sender, response_content
        )

        return response_message
