import random
from Assets.Scripts.domain.value_objects import Location

class MockGPSAdapter:
    """
    Adaptador de GPS de prueba/simulación.
    Genera ubicaciones aleatorias o con un patrón simple para simular movimiento.
    """
    def __init__(self, initial_location: Location):
        self._current_location = initial_location

    def get_current_location(self) -> Location:
        """
        Simula la obtención de la ubicación actual, con un pequeño desplazamiento.
        """
        # Simula un pequeño movimiento
        delta_lat = random.uniform(-0.0001, 0.0001)
        delta_lon = random.uniform(-0.0001, 0.0001)
        self._current_location = Location(
            latitude=self._current_location.latitude + delta_lat,
            longitude=self._current_location.longitude + delta_lon
        )
        return self._current_location
