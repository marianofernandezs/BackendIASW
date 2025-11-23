from Assets.Scripts.domain.repositories.user_repository import IUserRepository
from Assets.Scripts.domain.services.password_service import IPasswordService
from Assets.Scripts.domain.use_cases.register_user import IRegisterUserUseCase
from Assets.Scripts.application.use_cases.register_user_interactor import RegisterUserInteractor
from Assets.Scripts.infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository
from Assets.Scripts.infrastructure.security.bcrypt_password_service import BcryptPasswordService

class AppConfig:
    """
    Clase de configuración de la aplicación.
    Actúa como un contenedor de Inyección de Dependencias simple para
    inicializar y proveer las implementaciones concretas.
    """
    _user_repository: IUserRepository
    _password_service: IPasswordService
    _register_user_use_case: IRegisterUserUseCase

    def __init__(self):
        """
        Inicializa las dependencias de la aplicación.
        Aquí se decide qué implementaciones concretas usar.
        """
        self._user_repository = InMemoryUserRepository()
        self._password_service = BcryptPasswordService()
        self._register_user_use_case = RegisterUserInteractor(
            user_repository=self._user_repository,
            password_service=self._password_service
        )

    def get_user_repository(self) -> IUserRepository:
        """Obtiene la instancia del repositorio de usuarios."""
        return self._user_repository

    def get_password_service(self) -> IPasswordService:
        """Obtiene la instancia del servicio de contraseñas."""
        return self._password_service

    def get_register_user_use_case(self) -> IRegisterUserUseCase:
        """Obtiene la instancia del caso de uso de registro de usuario."""
        return self._register_user_use_case
