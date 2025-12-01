import logging
import uuid
from abc import ABC, abstractmethod
from decimal import Decimal

from django.db import transaction as db_transaction

from payments.models import PaymentTransaction, SavedPaymentMethod

logger = logging.getLogger("payments")


class PaymentGatewayService(ABC):
    """
    Interface for payment gateways.
    """

    @abstractmethod
    def process_payment(self, transaction_id: str, amount: Decimal, currency: str, card_details: dict, save_method: bool = False) -> dict:
        """Process a payment with card details."""
        raise NotImplementedError

    @abstractmethod
    def tokenize_card(self, card_details: dict) -> dict:
        """Tokenize card information."""
        raise NotImplementedError

    @abstractmethod
    def confirm_payment(self, gateway_reference_id: str) -> dict:
        """Confirm payment status with the gateway."""
        raise NotImplementedError


class MockPaymentGatewayService(PaymentGatewayService):
    """
    Mock gateway used for local development and tests.
    """

    def process_payment(self, transaction_id: str, amount: Decimal, currency: str, card_details: dict, save_method: bool = False) -> dict:
        logger.info("Simulating payment processing for transaction %s with %s %s", transaction_id, amount, currency)
        # Simulate a failure when card number starts with 4111
        if "card_number" in card_details and card_details["card_number"].startswith("4111"):
            logger.warning("Simulated payment failure for transaction %s", transaction_id)
            return {
                "status": False,
                "gateway_reference_id": f"mock_fail_{uuid.uuid4()}",
                "message": "Simulated failure for test card.",
            }

        token_data = self.tokenize_card(card_details) if save_method else None

        logger.info("Simulated payment success for transaction %s", transaction_id)
        return {
            "status": True,
            "gateway_reference_id": f"mock_success_{uuid.uuid4()}",
            "message": "Mock gateway processed payment successfully.",
            "token_data": token_data,
        }

    def tokenize_card(self, card_details: dict) -> dict:
        card_number = card_details.get("card_number", "************1234")
        last_four = card_number[-4:]
        brand = "Unknown"
        if card_number.startswith("4"):
            brand = "Visa"
        elif card_number.startswith("5"):
            brand = "Mastercard"

        expiration_month = card_details.get("expiry_month", "12")
        expiration_year = card_details.get("expiry_year", "2025")

        logger.info("Simulating card tokenization ****%s", last_four)
        return {
            "token": f"mock_token_{uuid.uuid4()}",
            "card_brand": brand,
            "last_four_digits": last_four,
            "expiration_date": f"{expiration_month}/{expiration_year}",
        }

    def confirm_payment(self, gateway_reference_id: str) -> dict:
        logger.info("Simulating payment confirmation for reference %s", gateway_reference_id)
        if "fail" in gateway_reference_id:
            return {"status": False, "message": "Simulated failure on confirmation."}
        return {"status": True, "message": "Simulated confirmation success."}


class PaymentProcessor:
    """
    High-level service to manage payment flow using a gateway implementation.
    """

    def __init__(self, gateway_service: PaymentGatewayService):
        self.gateway_service = gateway_service
        self.payment_method_service = PaymentMethodService()

    @db_transaction.atomic
    def initiate_payment(self, user_id: str, amount: Decimal, currency: str, card_details: dict, save_method: bool = False) -> PaymentTransaction:
        if amount <= 0:
            raise ValueError("El monto del pago debe ser positivo.")

        transaction = PaymentTransaction.objects.create(
            user_id=user_id,
            amount=amount,
            currency=currency,
            status=PaymentTransaction.PaymentStatus.PENDING,
        )
        logger.info("Transaction %s created for user %s. Status: PENDING.", transaction.id, user_id)

        try:
            gateway_response = self.gateway_service.process_payment(
                transaction_id=str(transaction.id),
                amount=amount,
                currency=currency,
                card_details=card_details,
                save_method=save_method,
            )

            transaction.gateway_id = gateway_response.get("gateway_reference_id")
            transaction.gateway_response = gateway_response

            if gateway_response.get("status"):
                transaction.status = PaymentTransaction.PaymentStatus.COMPLETED
                logger.info("Transaction %s completed. Gateway ref: %s.", transaction.id, transaction.gateway_id)

                token_data = gateway_response.get("token_data")
                if save_method and token_data:
                    self.payment_method_service.save_method(
                        user_id=user_id,
                        gateway_token=token_data["token"],
                        card_brand=token_data.get("card_brand"),
                        last_four=token_data.get("last_four_digits"),
                        exp_date=token_data.get("expiration_date"),
                        is_default=False,
                    )
                    logger.info("Tokenized payment method saved for user %s.", user_id)
            else:
                transaction.status = PaymentTransaction.PaymentStatus.FAILED
                logger.error("Transaction %s failed: %s", transaction.id, gateway_response.get("message", "Unknown error"))
                raise Exception(f"Fallo en la pasarela de pago: {gateway_response.get('message', 'Error desconocido')}")

        except Exception as e:
            transaction.status = PaymentTransaction.PaymentStatus.FAILED
            logger.error("Error processing payment for transaction %s: %s", transaction.id, e, exc_info=True)
            raise e
        finally:
            transaction.save()

        return transaction

    @db_transaction.atomic
    def handle_gateway_callback(self, transaction_id: str, gateway_response: dict, status: str) -> PaymentTransaction:
        try:
            transaction = PaymentTransaction.objects.get(id=transaction_id)
            logger.info("Handling callback for transaction %s. New status: %s.", transaction_id, status)

            transaction.gateway_response = gateway_response
            transaction.status = status
            transaction.save()
            return transaction
        except PaymentTransaction.DoesNotExist:
            logger.error("Transaction %s not found for callback.", transaction_id)
            raise ValueError(f"Transacción {transaction_id} no encontrada.")
        except Exception as e:
            logger.error("Error handling callback for transaction %s: %s", transaction_id, e, exc_info=True)
            raise e


class PaymentMethodService:
    """
    Service for managing saved payment methods.
    """

    def save_method(self, user_id: str, gateway_token: str, card_brand: str, last_four: str, exp_date: str, is_default: bool = False) -> SavedPaymentMethod:
        if SavedPaymentMethod.objects.filter(user_id=user_id, gateway_token=gateway_token).exists():
            logger.info("Payment method with token %s already exists for user %s.", gateway_token, user_id)
            return SavedPaymentMethod.objects.get(user_id=user_id, gateway_token=gateway_token)

        method = SavedPaymentMethod.objects.create(
            user_id=user_id,
            gateway_token=gateway_token,
            card_brand=card_brand,
            last_four_digits=last_four,
            expiration_date=exp_date,
            is_default=is_default,
        )
        logger.info("Payment method %s saved for user %s.", method.id, user_id)
        return method

    def get_saved_methods(self, user_id: str):
        return SavedPaymentMethod.objects.filter(user_id=user_id).order_by("-is_default", "-created_at")

    def delete_method(self, method_id: str, user_id: str):
        try:
            method = SavedPaymentMethod.objects.get(id=method_id, user_id=user_id)
            method_id_str = str(method.id)
            method.delete()
            logger.info("Payment method %s deleted for user %s.", method_id_str, user_id)
            return True
        except SavedPaymentMethod.DoesNotExist:
            logger.warning("Attempted to delete payment method %s for user %s that was not found or unauthorized.", method_id, user_id)
            return False

    def save_payment_method(self, user_id: str, payment_method_type: str, card_details: dict, is_default: bool = False):
        """
        Compatibility alias used by the Django shell call. Generates a token and persists the card.
        """
        gateway_token = card_details.get("token") or f"generated_token_{uuid.uuid4()}"
        brand = card_details.get("brand")
        last_four = card_details.get("last4") or card_details.get("last_four") or card_details.get("last_four_digits")
        exp_date = card_details.get("exp") or card_details.get("expiration_date")
        return self.save_method(
            user_id=user_id,
            gateway_token=gateway_token,
            card_brand=brand,
            last_four=last_four,
            exp_date=exp_date,
            is_default=is_default,
        )


class PaymentService:
    """
    Shell-friendly facade that wraps PaymentProcessor with the mock gateway.
    """

    def __init__(self):
        self.payment_processor = PaymentProcessor(gateway_service=MockPaymentGatewayService())

    def initiate_payment(self, payment_data: dict) -> PaymentTransaction:
        """
        Expects a dict with: user_id, amount, payment_method (unused in mock), card_details, optional currency/save_method.
        """
        user_id = payment_data.get("user_id")
        amount = Decimal(payment_data.get("amount"))
        currency = payment_data.get("currency", "USD")
        card_details = payment_data.get("card_details", {})
        save_method = bool(payment_data.get("save_method", False))
        return self.payment_processor.initiate_payment(
            user_id=user_id,
            amount=amount,
            currency=currency,
            card_details=card_details,
            save_method=save_method,
        )

    def handle_gateway_callback(self, transaction_id: str, status: str, gateway_response: dict | None = None) -> PaymentTransaction:
        gateway_response = gateway_response or {}
        return self.payment_processor.handle_gateway_callback(
            transaction_id=transaction_id,
            gateway_response=gateway_response,
            status=status,
        )
