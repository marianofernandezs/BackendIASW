from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer:
    """
    Serializador conceptual (no DRF).
    Representa un usuario o prepara datos para crearlo.
    """

    def __init__(self, data=None):
        self.data = data
        self.errors = {}
        self.valid = False

    def is_valid(self):
        if not self.data:
            self.errors["general"] = "No se enviaron datos."
            return False

        if "email" not in self.data:
            self.errors["email"] = "Email requerido."

        if "password" not in self.data:
            self.errors["password"] = "Contraseña requerida."

        self.valid = len(self.errors) == 0
        return self.valid

    @property
    def validated_data(self):
        if not self.valid:
            raise Exception("Llama primero a is_valid().")
        return self.data

    def to_representation(self, user: User):
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "date_joined": user.date_joined.isoformat(),
        }
