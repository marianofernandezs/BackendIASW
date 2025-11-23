import json
import os
from typing import Dict, Any

from Application.Interfaces.persistence_service import IPersistenceService

class JsonFilePersistenceService(IPersistenceService):
    """Implementación del servicio de persistencia usando archivos JSON."""

    def save_data(self, data: Dict[str, Any], file_path: str) -> None:
        """Guarda un diccionario de datos en un archivo JSON."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True) # Asegura que la ruta exista
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al guardar datos en '{file_path}': {e}")
            raise

    def load_data(self, file_path: str) -> Dict[str, Any]:
        """Carga datos desde un archivo JSON, retornando un diccionario."""
        if not self.data_exists(file_path):
            return {} # Retorna un diccionario vacío si el archivo no existe
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON desde '{file_path}': {e}")
            return {}
        except IOError as e:
            print(f"Error al cargar datos desde '{file_path}': {e}")
            raise

    def data_exists(self, file_path: str) -> bool:
        """Verifica si el archivo de persistencia existe."""
        return os.path.exists(file_path)

