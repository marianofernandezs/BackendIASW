from dataclasses import dataclass

@dataclass(frozen=True)
class AppSettings:
    """
    Clase de configuración de la aplicación (análogo a ScriptableObject para Unity).
    Contiene parámetros que pueden ser configurados o ajustados.
    """
    GPS_UPDATE_INTERVAL_SECONDS: int = 30
    DEFAULT_INITIAL_LATITUDE: float = 40.7128 # Ej. Nueva York
    DEFAULT_INITIAL_LONGITUDE: float = -74.0060 # Ej. Nueva York
    
    # Otros settings como conexión a DB, URLs de API, etc.
    DATABASE_URL: str = "sqlite:///./test.db"
    API_KEY_GOOGLE_MAPS: str = "your_google_maps_api_key_here"
