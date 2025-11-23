import random
import time
from application.interfaces.services import IAgentService

class MockAgentService(IAgentService):
    """Implementación de IAgentService que simula respuestas de agentes y bots."""
    def get_human_agent_response(self, user_message_content: str) -> str:
        """Simula una respuesta de agente humano."""
        time.sleep(0.5) # Simula un pequeño retardo
        responses = [
            f"Hola, soy tu agente de soporte. He recibido tu mensaje: '{user_message_content}'. ¿Podrías darme más detalles?",
            f"Entiendo tu situación con '{user_message_content}'. Estoy revisando cómo podemos ayudarte.",
            f"Gracias por contactar. Con respecto a '{user_message_content}', te ofrezco la siguiente solución..."
        ]
        return random.choice(responses)

    def get_bot_response(self, user_message_content: str) -> str:
        """Simula una respuesta de bot."""
        time.sleep(0.1) # Retardo mínimo para el bot
        responses = [
            f"He recibido tu mensaje: '{user_message_content}'. Por favor, espera mientras busco una respuesta.",
            f"Tu consulta sobre '{user_message_content}' es importante para nosotros. Nuestro equipo te atenderá pronto.",
            "Para problemas comunes, puedes visitar nuestra sección de Preguntas Frecuentes en el sitio web."
        ]
        return random.choice(responses)

    def get_available_agent_id(self) -> str | None:
        """Simula la disponibilidad de un agente humano."""
        # 70% de probabilidad de que haya un agente disponible en horario hábil
        if random.random() < 0.7:
            return f"agent_{random.randint(1, 5)}"
        return None
