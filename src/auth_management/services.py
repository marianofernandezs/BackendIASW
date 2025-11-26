from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class AuthService:

    @staticmethod
    def authenticate_user(email: str, password: str):
        """
        Intenta autenticar usando el email.
        Django por defecto autentica con username, por eso buscamos el usuario primero.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None  # email no existe

        # Django autentica con username
        return authenticate(username=user.username, password=password)
