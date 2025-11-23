from abc import ABC, abstractmethod

class IPasswordService(ABC):
    """
    Interfaz abstracta para un servicio de gestión de contraseñas.
    Define el contrato para operaciones de hashing y verificación.
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Hashea una contraseña en texto plano.
        :param password: Contraseña en texto plano.
        :return: Hash de la contraseña.
        """
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con un hash dado.
        :param plain_password: Contraseña en texto plano a verificar.
        :param hashed_password: Hash de la contraseña almacenado.
        :return: True si coinciden, False en caso contrario.
        """
        pass
