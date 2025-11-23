from dataclasses import dataclass
from datetime import datetime, time
import json

@dataclass
class SupportHoursConfig:
    """Configuración del horario de soporte (análogo a ScriptableObject)."""
    start_time_str: str = "09:00"
    end_time_str: str = "18:00"
    timezone: str = "UTC" # Considerar usar pytz o zoneinfo para zonas horarias reales

    @property
    def start_time(self) -> time:
        """Hora de inicio de soporte como objeto time."""
        h, m = map(int, self.start_time_str.split(':'))
        return time(h, m)

    @property
    def end_time(self) -> time:
        """Hora de fin de soporte como objeto time."""
        h, m = map(int, self.end_time_str.split(':'))
        return time(h, m)

    def is_within_business_hours(self, current_dt: datetime) -> bool:
        """Verifica si una fecha/hora dada está dentro del horario de soporte."""
        current_t = current_dt.time()
        # Asumiendo que el horario no cruza la medianoche para simplificar
        return self.start_time <= current_t <= self.end_time

    @classmethod
    def load_from_json(cls, filepath: str) -> 'SupportHoursConfig':
        """Carga la configuración desde un archivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

@dataclass
class ChatSettings:
    """Configuración general del chat (mensajes del bot, etc.)."""
    bot_greeting_message: str = "Hola, soy el asistente virtual. ¿En qué puedo ayudarte?"
    bot_out_of_hours_message: str = "Nuestro horario de soporte es de {start} a {end}. Te responderé con información básica por ahora."
    bot_default_response: str = "Entiendo. ¿Puedes darme más detalles sobre tu problema?"

    @classmethod
    def load_from_json(cls, filepath: str) -> 'ChatSettings':
        """Carga la configuración desde un archivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
