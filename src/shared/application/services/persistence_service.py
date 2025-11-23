from abc import ABC, abstractmethod
from typing import Dict, Any

class IPersistenceService(ABC):
    """Interfaz (ABC) para el servicio de persistencia genérico."""

    @abstractmethod
    def save_data(self, data: Dict[str, Any], file_path: str) -> None:
        """Guarda un diccionario de datos en una ruta de archivo."""
        pass

    @abstractmethod
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """Carga datos desde una ruta de archivo, retornando un diccionario."""
        pass

    @abstractmethod
    def data_exists(self, file_path: str) -> bool:
        """Verifica si el archivo de persistencia existe."""
        pass

