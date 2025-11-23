from dataclasses import dataclass

@dataclass(frozen=True)
class Location:
    """
    Objeto de valor que representa una ubicación geográfica.
    Inmutable.
    """
    latitude: float
    longitude: float
