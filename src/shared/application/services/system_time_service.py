from datetime import datetime
from application.interfaces.services import ITimeService

class SystemTimeService(ITimeService):
    """Implementación concreta de ITimeService que usa la hora del sistema."""
    def get_current_time(self) -> datetime:
        """Devuelve la hora y fecha actuales."""
        return datetime.now()
