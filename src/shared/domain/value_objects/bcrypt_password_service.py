import bcrypt

from Assets.Scripts.domain.services.password_service import IPasswordService

class BcryptPasswordService(IPasswordService):
    """
    Implementación de IPasswordService usando la librería bcrypt.
    """

    def hash_password(self, password: str) -> str:
        """
        Hashea una contraseña usando bcrypt.
        Asegura que el input es bytes antes de hashear.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña en texto plano contra un hash bcrypt.
        Asegura que ambos inputs son bytes para la verificación.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
