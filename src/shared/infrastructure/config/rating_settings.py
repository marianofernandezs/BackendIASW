from dataclasses import dataclass
import json

@dataclass(frozen=True)
class RatingSettings:
    """
    Clase de configuración para el sistema de calificación.
    Emula el patrón ScriptableObject de Unity, permitiendo definir
    parámetros de calificación de forma desacoplada y configurable.
    """
    min_estrellas: int = 1
    max_estrellas: int = 5
    permite_comentarios_vacios: bool = True

    @classmethod
    def load_from_json(cls, filepath: str):
        """Carga la configuración desde un archivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

    def to_json(self, filepath: str):
        """Guarda la configuración en un archivo JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=4)

# Ejemplo de uso:
# settings = RatingSettings(min_estrellas=1, max_estrellas=5)
# settings.to_json("rating_config.json")
# loaded_settings = RatingSettings.load_from_json("rating_config.json")

