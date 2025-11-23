import os
from datetime import datetime, timedelta

from domain.entities import User
from application.services.chat_service import ChatService
from application.services.persistence_manager import PersistenceManager
from application.services.event_bus import EventBus
from application.interfaces.repositories import (
    IMessageRepository, IUserRepository, IInventoryRepository, ICraftingRepository
)
from application.interfaces.services import IAgentService, ITimeService
from application.use_cases.chat_use_cases import (
    StartChatUseCase, SendMessageUseCase, HandleAgentResponseUseCase,
    ChatStarted, MessageReceived, AgentResponded, ChatEnded
)
from application.strategies.agent_response_strategy import (
    IAgentResponseStrategy, HumanAgentResponseStrategy, BotResponseStrategy
)
from infrastructure.repositories.json_repository import (
    JsonMessageRepository, JsonUserRepository, JsonInventoryRepository, JsonCraftingRepository
)
from infrastructure.services.system_time_service import SystemTimeService
from infrastructure.services.mock_agent_service import MockAgentService
from infrastructure.config.chat_config import SupportHoursConfig, ChatSettings

# --- Event Handlers (para observar el sistema) ---
def on_chat_started(event: ChatStarted):
    """Maneja el evento de inicio de chat."""
    print(f"\n[EVENT] Chat Iniciado: Sesión {event.session_id} para Usuario {event.user_id}")

def on_message_received(event: MessageReceived):
    """Maneja el evento de mensaje recibido."""
    print(f"  [EVENT] Mensaje recibido en sesión {event.session_id} de {event.message.sender.name}: {event.message.content[:50]}...")

def on_agent_responded(event: AgentResponded):
    """Maneja el evento de respuesta de agente/bot."""
    print(f"  [EVENT] {event.agent_type} respondió en sesión {event.session_id}: {event.response_message.content[:50]}...")

def on_chat_ended(event: ChatEnded):
    """Maneja el evento de fin de chat."""
    print(f"\n[EVENT] Chat Finalizado: Sesión {event.session_id}")

# --- Configuración (simulando carga de ScriptableObjects) ---
# Crear directorios para los datos si no existen
os.makedirs('data', exist_ok=True)

# Crear archivos de configuración de ejemplo si no existen
support_config_path = 'data/support_config.json'
chat_settings_path = 'data/chat_settings.json'

if not os.path.exists(support_config_path):
    with open(support_config_path, 'w', encoding='utf-8') as f:
        f.write(
            json.dumps({
                "start_time_str": "09:00",
                "end_time_str": "18:00",
                "timezone": "America/Mexico_City"
            }, indent=4)
        )

if not os.path.exists(chat_settings_path):
    with open(chat_settings_path, 'w', encoding='utf-8') as f:
        f.write(
            json.dumps({
                "bot_greeting_message": "Hola, soy el asistente virtual de [Mi Servicio]. ¿En qué puedo ayudarte hoy?",
                "bot_out_of_hours_message": "Nuestro horario de soporte es de {start} a {end} (hora local). Actualmente estamos fuera de horario. Un agente revisará tu consulta tan pronto como sea posible.",
                "bot_default_response": "Gracias por tu mensaje. Para poder ayudarte mejor, ¿podrías proporcionar más detalles o un número de ticket si lo tienes?"
            }, indent=4)
        )

# Cargar configuraciones
support_hours_config = SupportHoursConfig.load_from_json(support_config_path)
chat_settings = ChatSettings.load_from_json(chat_settings_path)


def setup_dependencies(simulate_out_of_hours: bool = False):
    """
    Configura todas las dependencias usando inyección manual.
    Permite simular escenarios fuera de horario de soporte.
    """
    # Repositorios
    message_repo: IMessageRepository = JsonMessageRepository()
    user_repo: IUserRepository = JsonUserRepository()
    inventory_repo: IInventoryRepository = JsonInventoryRepository() # Placeholder
    crafting_repo: ICraftingRepository = JsonCraftingRepository() # Placeholder

    # Persistence Manager
    persistence_manager = PersistenceManager(message_repo, user_repo, inventory_repo, crafting_repo)

    # Servicios
    agent_service: IAgentService = MockAgentService()
    
    # TimeService para simular horario
    time_service: ITimeService
    if simulate_out_of_hours:
        # Establece una hora fuera del horario de soporte (ej. 23:00)
        out_of_hours_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
        class MockTimeService(ITimeService):
            def get_current_time(self) -> datetime:
                return out_of_hours_time
        time_service = MockTimeService()
        print(f"\n[SIMULACIÓN] Hora actual configurada a {out_of_hours_time.strftime('%H:%M')} (fuera de horario).")
    else:
        time_service = SystemTimeService()
        print(f"\n[SIMULACIÓN] Hora actual configurada a la hora del sistema ({time_service.get_current_time().strftime('%H:%M')}).")


    # Event Bus
    event_bus = EventBus()
    event_bus.subscribe(ChatStarted, on_chat_started)
    event_bus.subscribe(MessageReceived, on_message_received)
    event_bus.subscribe(AgentResponded, on_agent_responded)
    event_bus.subscribe(ChatEnded, on_chat_ended)

    # Estrategias
    human_agent_strategy = HumanAgentResponseStrategy(agent_service, time_service, support_hours_config, chat_settings)
    bot_agent_strategy = BotResponseStrategy(agent_service, chat_settings) # No se usa directamente aquí, pero es una opción

    # Como la historia dice que si el chat es fuera de horario, responde bot,
    # la HumanAgentResponseStrategy ya contiene la lógica para delegar al bot.
    # Así que el caso de uso siempre usará la estrategia "humana" que decidirá.
    main_agent_strategy: IAgentResponseStrategy = human_agent_strategy

    # Casos de Uso
    start_chat_uc = StartChatUseCase(message_repo, user_repo, event_bus)
    send_message_uc = SendMessageUseCase(message_repo, event_bus)
    handle_agent_response_uc = HandleAgentResponseUseCase(message_repo, time_service, main_agent_strategy, event_bus)

    # Servicio de Chat (fachada)
    chat_service = ChatService(start_chat_uc, send_message_uc, handle_agent_response_uc)

    return chat_service, user_repo, persistence_manager, event_bus, time_service

def simulate_chat_scenario(scenario_name: str, simulate_out_of_hours: bool, user_id: str, user_name: str):
    """Función para simular un escenario de chat."""
    print(f"\n--- INICIO DE ESCENARIO: {scenario_name} ---")
    
    chat_service, user_repo, persistence_manager, event_bus, time_service = setup_dependencies(simulate_out_of_hours)

    # Asegurarse de que el usuario exista
    user = user_repo.get_by_id(user_id)
    if not user:
        user = User(id=user_id, name=user_name)
        user_repo.save(user)
        print(f"DEBUG: Usuario {user_name} creado y guardado.")

    print(f"DEBUG: Hora de simulación actual: {time_service.get_current_time().strftime('%Y-%m-%d %H:%M:%S')}")

    # Paso 1: Iniciar chat
    print(f"\n[{user_name}] Intentando iniciar chat...")
    session = chat_service.start_chat_session(user_id)
    print(f"[{user_name}] Sesión de chat iniciada (ID: {session.id}).")

    # Paso 2: Usuario envía un mensaje
    user_message_content = "Tengo un problema con la configuración de mi cuenta."
    print(f"\n[{user_name}] Envía: {user_message_content}")
    chat_service.send_user_message(session.id, user_message_content)

    # El send_user_message ya desencadenó la respuesta del agente/bot.
    # Podemos imprimir el historial para ver la respuesta.
    print(f"\n--- Historial de chat para {user_name} ---")
    for msg in session.messages:
        print(f"[{msg.timestamp.strftime('%H:%M')}] {msg.sender.name}: {msg.content}")

    # Simular otro mensaje
    user_message_content_2 = "¿Hay alguna forma de acelerar el proceso?"
    print(f"\n[{user_name}] Envía: {user_message_content_2}")
    chat_service.send_user_message(session.id, user_message_content_2)

    print(f"\n--- Historial de chat FINAL para {user_name} ---")
    # Recargar la sesión para obtener los últimos mensajes persistidos
    updated_session = persistence_manager.message_repo.get_by_id(session.id)
    if updated_session:
        for msg in updated_session.messages:
            print(f"[{msg.timestamp.strftime('%H:%M')}] {msg.sender.name}: {msg.content}")
    
    # En un sistema real, el chat se cerraría explícitamente o por inactividad
    # Aquí lo simularíamos al final del escenario para limpiar
    # event_bus.publish(ChatEnded(session_id=session.id)) # Descomentar si se quiere simular el fin

    print(f"\n--- FIN DE ESCENARIO: {scenario_name} ---")

if __name__ == "__main__":
    # Escenario 1: Chat con agente disponible (en horario hábil)
    simulate_chat_scenario(
        "Chat con agente disponible (dentro de horario hábil)",
        simulate_out_of_hours=False,
        user_id="user_001",
        user_name="Alice"
    )

    print("\n" + "="*80 + "\n") # Separador entre escenarios

    # Escenario 2: Chat fuera de horario (responde bot)
    simulate_chat_scenario(
        "Chat fuera de horario (responde bot)",
        simulate_out_of_hours=True,
        user_id="user_002",
        user_name="Bob"
    )
