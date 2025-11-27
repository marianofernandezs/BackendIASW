import uuid
from django.db import transaction
from .models import Order, DeliveryRating, OrderComment
from django.core.exceptions import ValidationError, ObjectDoesNotExist



class RatingService:
    """
    Servicio que encapsula la lógica de negocio para gestionar las calificaciones de entrega.
    La existencia de DeliveryRating es la ÚNICA fuente de verdad.
    """

    @staticmethod
    def get_order_for_rating(order_id: uuid.UUID) -> Order:
        """
        Recupera un pedido válido para calificación.
        Falla si no existe o si ya fue calificado.
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError("Pedido no encontrado.")

        if DeliveryRating.objects.filter(order=order).exists():
            raise ValueError("Este pedido ya fue calificado.")

        return order

    @staticmethod
    @transaction.atomic
    def create_delivery_rating(order_id: uuid.UUID, score: int, comment: str = None) -> DeliveryRating:
        """
        Crea una nueva calificación para un pedido.
        """
        order = RatingService.get_order_for_rating(order_id)

        rating = DeliveryRating.objects.create(
            order=order,
            score=score,
            comment=comment
        )

        return rating

    @staticmethod
    @transaction.atomic
    def mark_order_as_skipped(order_id: uuid.UUID) -> Order:
        """
        Marca explícitamente que el pedido fue omitido (sin crear DeliveryRating).
        Esto queda solo como evento de negocio sin persistir estado.
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError("Pedido no encontrado.")

        if DeliveryRating.objects.filter(order=order).exists():
            raise ValueError("No se puede omitir un pedido ya calificado.")

        return order

class OrderCommentService:
    """
    Servicio de negocio para gestionar comentarios de pedidos (HU12).
    """

    @staticmethod
    def create_comment(order_id: uuid.UUID, user, message: str) -> OrderComment:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ObjectDoesNotExist(f"Pedido con ID {order_id} no encontrado.")

        if not message or not message.strip():
            raise ValidationError("El comentario no puede estar vacío.")

        comment = OrderComment.objects.create(
            order=order,
            user=user,
            message=message.strip()
        )

        return comment
