from django.db import transaction
from django.shortcuts import get_object_or_404
from payment_methods.models import PaymentMethod

class PaymentMethodService:
    """
    Servicio que encapsula la lógica de negocio para gestionar métodos de pago.
    Aplica el principio de Responsabilidad Única (SRP) al centralizar las operaciones de PM.
    """

    def create_payment_method(
        self, user, token, brand, last_four_digits, expiry_month, expiry_year, consent_given
    ):
        """
        Crea y persiste un nuevo método de pago para un usuario si el consentimiento fue dado
        y el token no ha sido guardado previamente por este usuario.
        """
        if not consent_given:
            return None # Si no hay consentimiento, no se guarda el método de pago

        # Evitar duplicados por token, aunque el modelo ya tiene unique=True
        if PaymentMethod.objects.filter(user=user, token=token).exists():
            # Podríamos lanzar una excepción o simplemente retornar el existente
            return PaymentMethod.objects.get(user=user, token=token)

        with transaction.atomic():
            payment_method = PaymentMethod.objects.create(
                user=user,
                token=token,
                brand=brand,
                last_four_digits=last_four_digits,
                expiry_month=expiry_month,
                expiry_year=expiry_year,
                consent_given=True # Siempre True si llegamos a este punto y creamos
            )
            # Asegurar que solo un método de pago sea predeterminado
            if not user.payment_methods.exclude(pk=payment_method.pk).filter(is_default=True).exists():
                payment_method.is_default = True
                payment_method.save()
            return payment_method

    def get_user_payment_methods(self, user):
        """
        Recupera todos los métodos de pago guardados por un usuario.
        """
        return PaymentMethod.objects.filter(user=user).order_by('-is_default', 'brand')

    def get_payment_method_by_id(self, user, payment_method_id):
        """
        Recupera un método de pago específico por su ID para un usuario dado.
        """
        return get_object_or_404(PaymentMethod, user=user, id=payment_method_id)

    def delete_payment_method(self, user, payment_method_id):
        """
        Elimina un método de pago específico de un usuario.
        Retorna True si se eliminó, False si no se encontró o no pertenece al usuario.
        """
        payment_method = self.get_payment_method_by_id(user, payment_method_id)
        if payment_method:
            with transaction.atomic():
                payment_method.delete()
                # Lógica adicional, ej: si el eliminado era el predeterminado, asignar uno nuevo
                if payment_method.is_default:
                    remaining_methods = user.payment_methods.all()
                    if remaining_methods.exists():
                        first_method = remaining_methods.first()
                        first_method.is_default = True
                        first_method.save()
                return True
        return False

    def set_default_payment_method(self, user, payment_method_id):
        """
        Establece un método de pago como predeterminado para el usuario,
        desactivando el predeterminado anterior.
        """
        with transaction.atomic():
            # Desactivar el método de pago predeterminado actual
            PaymentMethod.objects.filter(user=user, is_default=True).update(is_default=False)

            # Establecer el nuevo método como predeterminado
            payment_method = self.get_payment_method_by_id(user, payment_method_id)
            if payment_method:
                payment_method.is_default = True
                payment_method.save()
                return payment_method
            return None
